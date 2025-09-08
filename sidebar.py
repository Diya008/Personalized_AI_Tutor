#new
import streamlit as st
from utils import storage
from datetime import datetime

def render_sidebar(current_page="pages/lesson_plan.py"):
    # --- Hide Default Sidebar Navigation and Style Icons ---
    st.markdown("""
        <style>
        [data-testid="stSidebarNav"] { display: none; }
        .icon-button {
            display: inline-block;
            margin: 0 5px;
            text-align: center;
            font-size: 24px;
            width: 50px;
            height: 50px;
            line-height: 50px;
            border-radius: 50%;
            background-color: #f0f0f0;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .icon-button:hover { background-color: #e0e0e0; }
        .icon-row {
            display: flex;
            justify-content: space-around;
            padding-top: 10px;
        }
        .session-summary {
            margin-top: 24px;
            font-size: 15px;
            background: #eff7ff;
            border-radius: 14px;
            padding: 14px 12px;
            color: #34547a;
            box-shadow: 0 2px 10px #b7cef911;
        }
        .session-heading {
            margin-bottom: 7px;
            font-size: 17px;
            font-weight: 623;
            color: #2359ad;
        }
        </style>
        """, unsafe_allow_html=True)

    # --- Icon Navigation Row ---
    st.sidebar.markdown('<div class="icon-row">', unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.sidebar.columns(5)
    if col1.button("🏠", key="icon_app", help="Home"):
        st.switch_page("app1.py")
    if col2.button("💬", key="icon_chatbot", help="Let's Talk"):
        st.switch_page("pages/chatbot.py")
    if col3.button("📚", key="icon_lesson_plan", help="Lesson Plan"):
        st.switch_page("pages/lesson_plan.py")
    if col4.button("▶️", key="icon_youtube", help="Youtube"):
        st.switch_page("pages/explain_youtube.py")
    if col5.button("📜", key="icon_history", help="History"):
        st.switch_page("pages/history.py")
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

    # --- Delete plan button shown on lesson plan page when a plan is selected from session ---
    if current_page == "pages/lesson_plan.py":
        current_plan = st.session_state.get("current_plan_name", None)
        if current_plan and current_plan != "-- New Plan --" and current_plan.strip() != "":
            if st.sidebar.button("🗑️ Delete Current Lesson Plan"):
                all_plans = storage.load_all_lesson_plans()
                if current_plan in all_plans:
                    del all_plans[current_plan]
                    storage.save_all_lesson_plans(all_plans)
                    st.sidebar.success(f"Deleted lesson plan '{current_plan}'")
                    # Reset session state after deletion
                    st.session_state.current_plan_name = ""
                    st.session_state.lesson_plan = []
                    st.rerun()  

    # --- Previous Session Summary (only show on app.py page) ---
    if current_page == "app1.py":
        chat_history = storage.load_chat_history()
        last_summary = ""
        last_date = ""
        if chat_history:
            history_by_date = {}
            for msg in chat_history:
                try:
                    date_str = datetime.fromisoformat(msg["timestamp"]).strftime("%Y-%m-%d")
                    history_by_date.setdefault(date_str, []).append(msg)
                except Exception:
                    continue
            recent_date = sorted(history_by_date.keys(), reverse=True)[0]
            recent_msgs = history_by_date[recent_date]
            summary_lines = [
                msg.get("content", "").strip()
                for msg in recent_msgs
                if msg["role"] == "assistant" and msg.get("content", "").strip()
            ]
            if summary_lines:
                last_summary = "\n\n".join(summary_lines[-2:])
                last_date = recent_date

        if last_summary:
            st.sidebar.markdown(f"""
                <div class="session-summary">
                    <div class="session-heading">🕑 Last Session Recap ({last_date})</div>
                    {last_summary}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.sidebar.markdown("""
                <div class="session-summary">
                    <div class="session-heading">🕑 Last Session Recap</div>
                    No recap available yet 😊
                </div>
            """, unsafe_allow_html=True)