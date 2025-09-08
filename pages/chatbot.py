#new
import streamlit as st
import json
import re
from datetime import datetime
from openai import OpenAI
from sidebar import render_sidebar
from utils import storage

#Save message to persistent history on every event
def save_message(role, content):
    if role != "system":
        msg = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "plan_name": st.session_state.get("current_plan_name", "Unknown Plan")
        }
        history = storage.load_chat_history()
        history.append(msg)
        storage.save_chat_history(history)

# --- Page setup ---
st.set_page_config(page_title="Let's talk", page_icon="💬", layout="wide")
st.title("💬 Let's Talk")
st.write("Talk to your AI teaching assistant for the selected lesson task.")

with open('utils/config.json', 'r') as config_file:
    config = json.load(config_file)
GEMINI_MODEL = config.get('gemini_model_name', 'gemini-1.5-flash')
TEMPERATURE = config.get('temperature', 0.7)
LANGUAGE = config.get('language', 'English')

def get_gemini_client():
    return OpenAI(
        api_key=config.get('api_key', "Your-API-Key-Here"),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

def generate_content_and_quiz_for_task(task):
    prompt = f"""
The user's current lesson task is: {task}
Generate:
1. A simple teaching explanation similar to how geekofgeeks or w3schools would explain this topic.
2. ONE sentence inviting user questions about this topic.
3. Four quiz questions covering key ideas from this task, each as a JSON array:
   [question, correct_answer, [option1, option2, option3, option4]]

Format your output as a valid JSON object like this:

{{
  "lesson": "...",
  "invite": "...",
  "quiz": [
    ["Q1", "A1", ["A1", "Distractor1", "Distractor2", "Distractor3"]],
    ["Q2", "A2", ["A2", "Distractor1", "Distractor2", "Distractor3"]],
    ["Q3", "A3", ["A3", "Distractor1", "Distractor2", "Distractor3"]],
    ["Q4", "A4", ["A4", "Distractor1", "Distractor2", "Distractor3"]]
  ]
}}
    """
    client = get_gemini_client()
    response = client.chat.completions.create(
        model=GEMINI_MODEL,
        messages=[
            {"role": "system", "content": "You generate teaching explanations and quiz in strict JSON format only."},
            {"role": "user", "content": prompt}
        ],
        temperature=TEMPERATURE
    )
    output = response.choices[0].message.content

    # Defensive parsing
    try:
        data = json.loads(output)
        lesson = data.get("lesson", "")
        invite = data.get("invite", "")
        quiz = data.get("quiz", [])
        return lesson, invite, quiz
    except Exception:
        json_match = re.search(r'\{.*\}', output, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group())
                lesson = data.get("lesson", "")
                invite = data.get("invite", "")
                quiz = data.get("quiz", [])
                return lesson, invite, quiz
            except Exception:
                st.error(f"AI output could not be parsed correctly: {output}")
        st.error("LLM did not return valid JSON:\n" + output)
        return "Error generating lesson for this task (JSON malformed).", "", []

if "active_task" not in st.session_state or "active_task_index" not in st.session_state:
    st.error("No active task selected. Return to the lesson plan and pick a task to practice.")
    if st.button("Go to lesson page"):
        st.switch_page("pages/lesson_plan.py")
    st.stop()

task = st.session_state.active_task
task_idx = st.session_state.active_task_index

if ("lesson_content" not in st.session_state or
    "quiz_questions" not in st.session_state or
    st.session_state.lesson_content_task != task):

    lesson, invite, quiz_raw = generate_content_and_quiz_for_task(task)
    quiz_objs = []
    for q in quiz_raw:
        quiz_objs.append({
            "question": q[0],
            "answer": q[1],
            "options": q[2],
            "user_answer": ""
        })

    st.session_state.lesson_content = lesson
    st.session_state.lesson_invite = invite
    st.session_state.quiz_questions = quiz_objs
    st.session_state.lesson_content_task = task

st.write(f"### Lesson Topic: {task}")
st.write(st.session_state.lesson_content)
st.write(st.session_state.lesson_invite)

if "messages" not in st.session_state:
    st.session_state.system_prompt = {
        "role": "system",
        "content": f"""
You are a friendly expert tutor. Only answer about this task: "{task}".
- Provide clear explanations, Q&A, and guidance strictly for this task.
- Ignore any unrelated question. Answers should be clear and concise.
- Use simple language and examples.
- If the user asks something outside this topic, politely say you can only help with this task
"""
    }
    st.session_state.messages = [st.session_state.system_prompt]

render_sidebar()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Type your message here...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    save_message("user", user_input) 
    with st.chat_message("user"):
        st.write(user_input)

    with st.spinner("Thinking..."):
        messages_for_api = [st.session_state.system_prompt] + [
            m for m in st.session_state.messages if m["role"] != "system"
        ]
        bot_reply = OpenAI(
            api_key=config.get('api_key', "Your-API-Key-Here"),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        ).chat.completions.create(
            model=GEMINI_MODEL,
            messages=messages_for_api,
            temperature=TEMPERATURE
        ).choices[0].message.content

    with st.chat_message("assistant"):
        st.write(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    save_message("assistant", bot_reply)  

#Initialize show_quiz flag if not set
if "show_quiz" not in st.session_state:
    st.session_state.show_quiz = False

if not st.session_state.show_quiz:
    if st.button("Show Quiz"):
        st.session_state.show_quiz = True

if st.session_state.show_quiz:
    st.divider()
    st.subheader("📝 Quiz: Answer the following to complete the task.")

    correct_count = 0
    for i, q in enumerate(st.session_state.quiz_questions):
        options = q.get("options", [q["answer"]])
        key_name = f"quiz_{i}"
        if "user_answer" not in q or q["user_answer"] not in options:
            st.session_state.quiz_questions[i]["user_answer"] = ""

        selected_option = st.radio(
            f"Q{i+1}: {q['question']}",
            options,
            key=key_name,
            index=options.index(q["user_answer"]) if q["user_answer"] in options else None
        )
        st.session_state.quiz_questions[i]["user_answer"] = selected_option
        if selected_option != "":
            if selected_option == q["answer"]:
                st.success("Correct!")
                correct_count += 1
            else:
                st.error("Wrong answer.")

    quiz_complete = correct_count == len(st.session_state.quiz_questions)
    if quiz_complete:
        st.success("Quiz completed! You can now mark this task as done in the lesson plan.")
        if "quiz_status" not in st.session_state:
            st.session_state.quiz_status = {}
        st.session_state.quiz_status[f"{task_idx[0]}_{task_idx[1]}"] = True
        st.session_state.quiz_passed = True

        if st.button("Go to next lesson"):
            st.switch_page("pages/lesson_plan.py")
    else:
        st.info(f"Answer all quiz questions correctly to unlock completion. {correct_count}/{len(st.session_state.quiz_questions)} correct.")