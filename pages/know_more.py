#new
import streamlit as st
from openai import OpenAI
import json

with open('utils/config.json', 'r') as config_file:
    config = json.load(config_file)

GEMINI_MODEL = config.get('gemini_model_name', 'gemini-1.5-flash')
TEMPERATURE = config.get('temperature', 0.7)

def get_gemini_client():
    return OpenAI(
        api_key=config.get('api_key', 'Your-API-Key-Here'),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

st.title("🤖 Concept Explanation Chatbot")

concept = st.session_state.get("active_query", "").strip()

if not concept:
    st.warning("No concept selected. Please select a concept from the lesson plan.")
    if st.button("Go to lesson page"):
        st.switch_page("pages/lesson_plan.py")
else:
    st.markdown(f"### Explaining: **{concept}**")


    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("Ask about this concept or enter a related question:")

    client = get_gemini_client()

    def generate_explanation(prompt):
        messages = [
            {"role": "system", "content": "You are an expert tutor providing clear and concise explanations.Answer in simple terms to any question associated with the given concept.If relevant, provide examples"},
            {"role": "user", "content": prompt}
        ]
        response = client.chat.completions.create(
            model=GEMINI_MODEL,
            messages=messages,
            temperature=TEMPERATURE
        )
        return response.choices[0].message.content

    if user_input:
        st.session_state.chat_history.append({"user": user_input})
        explanation = generate_explanation(f"Explain the following concept in simple terms:\n\n{user_input}")
        st.session_state.chat_history.append({"bot": explanation})

    # Display chat history
    for chat in st.session_state.chat_history:
        if "user" in chat:
            st.markdown(f"**You:** {chat['user']}")
        if "bot" in chat:
            st.markdown(f"**Tutor:** {chat['bot']}")

    if not st.session_state.chat_history:
        expl = generate_explanation(f"Explain the concept: {concept}")
        st.session_state.chat_history.append({"bot": expl})
        st.rerun()