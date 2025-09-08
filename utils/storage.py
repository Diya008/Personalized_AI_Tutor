#new
import json
import streamlit as st
import os
from datetime import datetime

LESSON_PLANS_FILE = "assets/lesson_plans.json"  #used to store multiple lesson plans
USER_INPUTS_FILE = "assets/lesson_plan_inputs.json" 
CHAT_HISTORY_FILE = "assets/chat_history.json"

def save_lesson_plan_inputs(inputs):
    with open(USER_INPUTS_FILE, "w") as f:
        json.dump(inputs, f)

def load_lesson_plan_inputs():
    try:
        with open(USER_INPUTS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

# --- Multiple lesson plan logic ---
def load_all_lesson_plans():
    try:
        with open(LESSON_PLANS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_all_lesson_plans(all_plans):
    with open(LESSON_PLANS_FILE, "w") as f:
        json.dump(all_plans, f)

def add_lesson_plan(plan_name, plan_json):
    all_plans = load_all_lesson_plans()
    all_plans[plan_name] = plan_json  # Save full lesson plan JSON (includes 'lesson_plan' and 'know_more')
    save_all_lesson_plans(all_plans)

def load_lesson_plan(plan_name=None):
    plans = load_all_lesson_plans()
    if plan_name and plan_name in plans:
        return plans[plan_name]  # Full JSON with 'lesson_plan' and 'know_more'
    if plans:
        latest = sorted(plans.keys())[-1]
        return plans[latest]
    return {}

def get_lesson_plan_names():
    return list(load_all_lesson_plans().keys())

def get_lesson_plan_assignments(plan_json):
    # Flatten assignment structure for rendering
    if "lesson_plan" in plan_json:
        return [
            {"week_or_day": key,
             "assignments": [{"title": task, "completed": False} for task in value]}
            for key, value in plan_json["lesson_plan"].items()
        ]
    return []

# Legacy: preserve single-plan file usage if needed elsewhere
def save_lesson_plan(plan):
    add_lesson_plan(f"Plan_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}", plan)

# --- Chat History ---
def load_chat_history():
    try:
        with open(CHAT_HISTORY_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_chat_history(messages):
    try:
        with open(CHAT_HISTORY_FILE, "w") as f:
            json.dump(messages, f)
    except Exception as e:
        st.error(f"Error saving chat history: {e}")