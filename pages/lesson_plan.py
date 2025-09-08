import streamlit as st
from utils import storage
from sidebar import render_sidebar
import json
import re
from openai import OpenAI
import PyPDF2
from datetime import datetime

st.set_page_config(page_title="Lesson Plan", page_icon="📚", layout="wide")
render_sidebar()

with open('utils/config.json', 'r') as config_file:
    config = json.load(config_file)
GEMINI_MODEL = config.get('gemini_model_name', 'gemini-1.5-flash')
TEMPERATURE = config.get('temperature', 0.7)
LANGUAGE = config.get('language', 'English')

def get_gemini_client():
    return OpenAI(
        api_key="Your-API-Key-Here",
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

# Load all plan names, always show -- New Plan --
all_plan_names = storage.get_lesson_plan_names()
plan_options = ["-- New Plan --"] + all_plan_names if all_plan_names else ["-- New Plan --"]
selected_old_plan = st.sidebar.selectbox("Select a previously saved plan to load", plan_options)

# If New Plan selected, ask for plan name input
if selected_old_plan == "-- New Plan --":
    plan_name_input = st.sidebar.text_input("Enter new lesson plan name:", value="")
else:
    plan_name_input = selected_old_plan

# Load plan in session state
if "lesson_plan" not in st.session_state or st.session_state.get("current_plan_name", "") != plan_name_input:
    if selected_old_plan != "-- New Plan --":
        lesson_plan_json = storage.load_lesson_plan(selected_old_plan)
        st.session_state.lesson_plan_json = lesson_plan_json or {}
        st.session_state.current_plan_name = selected_old_plan
        st.session_state.lesson_plan = storage.get_lesson_plan_assignments(lesson_plan_json or {})
    else:
        st.session_state.lesson_plan_json = {}
        st.session_state.lesson_plan = []
        st.session_state.current_plan_name = plan_name_input


if "lesson_plan_inputs" not in st.session_state:
    saved_inputs = storage.load_lesson_plan_inputs()
    st.session_state.lesson_plan_inputs = saved_inputs or {
        "user_level": "Beginner",
        "learning_period": "1 Month",
        "user_goals": "",
        "topics": "",
        "youtube_links": "",
        "pdf_texts": ""
    }

st.title("📚 Lesson Plan")
st.write("You can edit your plan by removing or adding items. Press 'Practice' to start lesson on the selected topic.")
st.write("Upload PDFs, or specify topics to guide lesson plan generation.")

with st.sidebar:
    st.header("📚 Generate a Lesson Plan")
    user_level = st.selectbox(
        "Select your level:",
        ["Beginner", "Intermediate", "Advanced"],
        index=["Beginner", "Intermediate", "Advanced"].index(st.session_state.lesson_plan_inputs.get("user_level", "Beginner"))
    )
    learning_period = st.selectbox(
        "Study duration:",
        ["1 Week", "1 Month", "3 Months"],
        index=["1 Week", "1 Month", "3 Months"].index(st.session_state.lesson_plan_inputs.get("learning_period", "1 Month"))
    )
    user_goals = st.text_area("Your learning goals:", value=st.session_state.lesson_plan_inputs.get("user_goals", ""))
    topics = st.text_area("Specific topics (comma separated):", value=st.session_state.lesson_plan_inputs.get("topics", ""))
    # youtube_links = st.text_area("YouTube video links (one URL per line):", value=st.session_state.lesson_plan_inputs.get("youtube_links", ""))
    uploaded_files = st.file_uploader("Upload supporting PDF files (optional):", type=['pdf'], accept_multiple_files=True)

    if st.button("📜 Generate Lesson Plan"):
        pdf_texts = ""
        if uploaded_files:
            for uploaded_file in uploaded_files:
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if text:
                        pdf_texts += text + "\n"

        st.session_state.lesson_plan_inputs = {
            "user_level": user_level,
            "learning_period": learning_period,
            "user_goals": user_goals,
            "topics": topics,
            # "youtube_links": youtube_links,
            "pdf_texts": pdf_texts
        }
        storage.save_lesson_plan_inputs(st.session_state.lesson_plan_inputs)

        client = get_gemini_client()

        lesson_prompt = f"""
        You are an AI that generates structured **lesson plans** for learning {topics} based on the information present in{pdf_texts}.
          - The user is at **{user_level}** level.
          - The lesson plan duration is **{learning_period}**.
          - The learning goals are: "{user_goals}".

          Your task:
          1. Generate the lesson plan in the following JSON format only (no additional explanations):

{{
  "lesson_plan": {{
    "Week 1 - Topic": ["Task 1", "Task 2"],
    "Week 2 - Topic": ["Task 1", "Task 2"]
  }},
  "know_more": [
     "Concept 1 the user should also learn which relates to the above topics",
     "Concept 2 another important related concept to support learning"
  ]
}}

The field "know_more" MUST ALWAYS be present as a list of at least two important related concepts that the user should additionally learn, based on the topics and pdf_texts provided.

If there are no missing or related important concepts, return an message saying "All topics covered" for "know_more".

            5. Use exactly the specified JSON format, return only valid JSON with no extra text.
            6. If the duration is less than 2 weeks, use "Day X - Topic" format.
            7. If duration is 1 week, only 7 days.
            8. If duration is 2 weeks or more, use "Week X - Topic" format.
            9. Each day/week should have at least 2 tasks.

Begin now.
"""

        with st.spinner("Generating lesson plan..."):
            response = client.chat.completions.create(
                model=GEMINI_MODEL,
                messages=[
                    {"role": "system", "content": "You generate structured JSON lesson plans only."},
                    {"role": "user", "content": lesson_prompt}
                ],
                temperature=TEMPERATURE
            )

        json_match = re.search(r'\{.*\}', response.choices[0].message.content, re.DOTALL)
        if json_match:
            try:
                lesson_plan_json = json.loads(json_match.group())
                if "lesson_plan" in lesson_plan_json:
                    formatted_plan = [
                        {"week_or_day": key, "assignments": [{"title": task, "completed": False} for task in value]}
                        for key, value in lesson_plan_json["lesson_plan"].items()
                    ]
                    st.session_state.lesson_plan = formatted_plan
                    st.session_state.lesson_plan_json = lesson_plan_json  # Save full JSON for displaying know_more

                    # Show know_more in sidebar immediately after generation
                    know_more = lesson_plan_json.get("know_more", [])
                    if know_more:
                        st.sidebar.markdown("### 📖 Know More - Important Concepts You Should Also Learn")
                        for concept in know_more:
                            st.sidebar.markdown(f"- {concept}")

                    if plan_name_input.strip():
                        storage.add_lesson_plan(plan_name_input.strip(), lesson_plan_json)
                        st.session_state.current_plan_name = plan_name_input.strip()
                    else:
                        plan_name = f"Plan_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
                        storage.add_lesson_plan(plan_name, lesson_plan_json)
                        st.session_state.current_plan_name = plan_name

                    st.success(f"Lesson plan '{st.session_state.current_plan_name}' generated and saved.")
                    st.rerun()
                else:
                    st.error("Error: AI response did not include 'lesson_plan' key. Try again.")
            except json.JSONDecodeError:
                st.error("Error: AI response was not valid JSON. Try again.")
        else:
            st.error("Error: AI did not return JSON. Please try again.")


if not st.session_state.lesson_plan:
    st.warning("No lesson plan available. Generate one from the sidebar!")
else:
    corrected_plan = []
    for entry in st.session_state.lesson_plan:
        if isinstance(entry, dict) and "week_or_day" in entry and "assignments" in entry:
            corrected_plan.append(entry)
    if corrected_plan != st.session_state.lesson_plan:
        st.session_state.lesson_plan = corrected_plan
        storage.add_lesson_plan(st.session_state.current_plan_name, st.session_state.lesson_plan_json)

    quiz_status = st.session_state.get("quiz_status", {})

    for i, lesson in enumerate(st.session_state.lesson_plan):
        st.markdown(f"### 🔹 {lesson['week_or_day']}")
        for j, assignment in enumerate(lesson["assignments"]):
            col1, col2, col3 = st.columns([0.7, 0.15, 0.15])
            is_quiz_complete = quiz_status.get(f"{i}_{j}", False)

            with col1:
                completed = st.checkbox(
                    assignment["title"],
                    assignment["completed"],
                    key=f"lesson_{i}_assignment_{j}",
                    disabled=not is_quiz_complete
                )
                if completed != assignment["completed"]:
                    st.session_state.lesson_plan[i]["assignments"][j]["completed"] = completed
                    storage.add_lesson_plan(st.session_state.current_plan_name, st.session_state.lesson_plan_json)

            with col2:
                if is_quiz_complete:
                    st.button("✅ Completed", key=f"done_{i}_{j}", disabled=True)
                else:
                    if st.button("▶️ Practice", key=f"play_{i}_{j}"):
                        st.session_state.active_task = assignment["title"]
                        st.session_state.active_task_index = (i, j)
                        st.session_state.quiz_passed = False
                        st.switch_page("pages/chatbot.py")

            with col3:
                if st.button("❌", key=f"delete_{i}_{j}"):
                    del st.session_state.lesson_plan[i]["assignments"][j]
                    storage.add_lesson_plan(st.session_state.current_plan_name, st.session_state.lesson_plan_json)
                    st.experimental_rerun()

    if "lesson_plan_json" in st.session_state:
        know_more = st.session_state.lesson_plan_json.get("know_more", [])
        if know_more:
            st.markdown("## 📖 Know More – Important Concepts You Should Also Learn")
            for idx, concept in enumerate(know_more):
                if st.button(concept, key=f"know_more_{idx}"):
                    st.session_state.active_query = concept
                    st.switch_page("pages/know_more.py")