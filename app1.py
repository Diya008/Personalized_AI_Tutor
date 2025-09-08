import streamlit as st
from utils import storage
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(page_title="Personalized AI Tutor", page_icon="🪐", layout="wide")

# Load all lesson plans to support multi-plan setup
all_plans = storage.load_all_lesson_plans()

# Select a current lesson plan (latest if none selected)
if "current_plan_name" not in st.session_state:
    if all_plans:
        latest_plan_name = sorted(all_plans.keys())[-1]
        st.session_state.current_plan_name = latest_plan_name
        st.session_state.lesson_plan = all_plans[latest_plan_name]
    else:
        st.session_state.current_plan_name = ""
        st.session_state.lesson_plan = []
else:
    # If already set, load that plan or fallback empty plan
    plan = all_plans.get(st.session_state.current_plan_name, [])
    st.session_state.lesson_plan = plan

lesson_plan = st.session_state.lesson_plan

#flatten lesson plan JSON if needed ---
if isinstance(lesson_plan, dict):
    if "lesson_plan" in lesson_plan:
        lesson_plan = [
            {"week_or_day": key, "assignments": [
                {"title": task, "completed": False} if isinstance(task, str) else task
                for task in value]
            }
            for key, value in lesson_plan["lesson_plan"].items()
        ]
    else:
        lesson_plan = []

#calculating user progress
total_tasks = sum(len(week['assignments']) for week in lesson_plan)
completed_tasks = sum(
    1 for week in lesson_plan for task in week['assignments'] if task.get('completed', False)
)
progress = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

# --- Improved CSS Styling ---
with open("css/style.css") as f:
    css = f.read()

# Inject CSS + dynamic progress
st.markdown(
    f"""
    <style>
    {css}
    .rocket-emoji {{
        position: absolute;
        left: calc(min(92%, max(4%, {progress}%)));
        top: 7px;
        font-size: 2.1rem;
        transition: left 0.5s cubic-bezier(.7,1.2,.8,1);
        filter: drop-shadow(0px 0px 8px #aaf9fcaa);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

from sidebar import render_sidebar
render_sidebar(current_page="app1.py")

st.markdown(
    f"""
    <div class="hero">
        <img class="tutor-avatar" src="https://cdn-icons-png.flaticon.com/512/4140/4140037.png" alt="AI Tutor">
        <div style="margin-left:145px;">
            <div class="hero-headline">🧑‍🏫 Personalized AI Tutor</div>
            <div class="hero-sub">
            Welcome back! <b>I'm here to guide your learning journey.</b><br>
            <span style="font-size:1.09rem;color:#4971b9;">What would you like to do today?</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True
)

# ---- GLASS NAV BUTTONS ----
st.markdown('<div class="glass-nav">', unsafe_allow_html=True)
cols = st.columns([1,1,1,1])
navs = [("💬 Chat with teaching assistant", "main_chatbot", "pages/chatbot.py"),
        ("📚 Review your lessons plan", "main_lesson_plan", "pages/lesson_plan.py"),
        ("▶️ Explain a Youtube video", "main_ty_explanation", "pages/explain_youtube.py"),
        ("📜 Look through past lessons", "main_history", "pages/history.py")]
for idx, (lbl, key, page) in enumerate(navs):
    with cols[idx]:
        with st.container():
            st.markdown('<div class="glass-button">', unsafe_allow_html=True)
            if st.button(lbl, key=key):
                st.session_state.current_plan_name = st.session_state.current_plan_name if "current_plan_name" in st.session_state else ""
                st.switch_page(page)
            st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---- PROGRESS BAR ----
st.subheader("🚀 Your Learning Journey", divider="gray")
st.markdown('<div class="learn-bar"></div>', unsafe_allow_html=True)
with open("css/progressbar.css") as f:
    css = f.read()
st.markdown(
    f"""
    <style>
    {css}
    .rocket {{
        position: absolute;
        top: 50%;
        left: {progress}%;
        width: 50px;
        height: 50px;
        background-image: url('https://www.iconpacks.net/icons/2/free-rocket-icon-3432-thumb.png');
        background-size: cover;
        transform: translate(-50%, -50%);
        transition: left 0.5s ease-in-out;
    }}
    </style>
    <div class="space-road">
        <div class="rocket"></div>
    </div>
    <p style="text-align: center; font-size: 18px;">{completed_tasks} out of {total_tasks} lessons completed ({progress:.2f}% 🚀)</p>
    """,
    unsafe_allow_html=True
)

if progress == 0:
    st.info("🔭 Ready for liftoff? Start your learning journey above!")
elif progress < 50:
    st.success("🌱 You're making real progress! Every completed lesson grows your skills.")
elif progress < 100:
    st.success("🎯 Fluent horizons ahead! Only a few lessons left. Keep it up, superstar!")
else:
    st.balloons()
    st.success("🏁 Congratulations, you finished your mission! 🚀")

st.markdown("""
    <div class="motive-tip">
        “Success in learning is built one step at a time. <br>
        Keep practicing—your tutor is here for you!”
    </div>
""", unsafe_allow_html=True)