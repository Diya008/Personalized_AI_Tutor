#new
import streamlit as st
import json
from datetime import datetime
from sidebar import render_sidebar
from utils import storage

st.set_page_config(page_title="Lesson History", page_icon="📜")
st.title("📜 Lesson History")
st.write("Look through your previous lessons.")
render_sidebar()

# Load all lesson plans to get names for filtering
all_plans = storage.load_all_lesson_plans()
plan_names = list(all_plans.keys())
selected_plan = st.sidebar.selectbox("Select lesson plan to view history for:", ["All Plans"] + plan_names)

st.sidebar.header("📜 History of your lessons")

chat_history = storage.load_chat_history()

# Filter chat history by selected plan if applicable
if selected_plan != "All Plans":
    filtered_history = [msg for msg in chat_history if msg.get("plan_name") == selected_plan]
else:
    filtered_history = chat_history

history_by_date = {}
invalid_timestamps = []

for idx, msg in enumerate(filtered_history):
    try:
        msg_time = datetime.fromisoformat(msg["timestamp"])
        date_str = msg_time.strftime("%Y-%m-%d")  # Extract date only
        # Append index as well for unique keys
        history_by_date.setdefault(date_str, []).append((idx, msg))
    except Exception:
        invalid_timestamps.append(msg.get("timestamp", ""))  # Track bad timestamps


if not history_by_date:
    st.warning("No conversation history available.")
else:
    for date, messages in sorted(history_by_date.items(), reverse=True):
        with st.expander(f"📅 {date}"):
            for idx, msg in messages:
                role = "👤 User" if msg["role"] == "user" else "🤖 Chatbot"
                col1, col2 = st.columns([0.95, 0.05])
                with col1:
                    st.markdown(f"**{role}:** {msg['content']}")
                with col2:
                    if st.button("❌", key=f"delete_msg_{idx}"):
                        # Delete message from chat history by index
                        chat_history.pop(idx)
                        storage.save_chat_history(chat_history)
                        st.switch_page("pages/history.py")  # Refresh page after deletion

if invalid_timestamps:
    st.error(f"Skipped messages with invalid timestamps: {invalid_timestamps}")