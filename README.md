# 🎓 Personalized AI Tutor

## 📌 Overview

**Personalized AI Tutor** is an intelligent, AI-powered learning assistant built with **Streamlit** and **Google’s Gemini models**. It delivers structured learning experiences through interactive lesson plans, AI-driven quizzes, conversational practice, and YouTube video explanations—all tailored to support effective self-paced learning.

---

## 🚀 Key Features

* 🤖 **AI Chatbot Tutor** – Real-time AI-powered conversations for interactive learning.
* 📑 **Lesson Plans** – Auto-generated structured learning paths.
* 🎥 **YouTube Explanation** – Paste a YouTube link and receive simplified explanations.
* 📝 **AI-Generated Quizzes** – Topic-specific quizzes to reinforce knowledge.
* 📜 **Lesson History** – Review past conversations and track learning progress.

---

## 🏗️ Tech Stack

* **Frontend:** Streamlit (rapid UI prototyping)
* **Backend:** Google Gemini Models (LLM-powered tutor)
* **Data Storage:** Local JSON files (user history, lesson plans, vocabulary)
* **UI Customization:** CSS & HTML enhancements

---

## 📂 Project Structure

```plaintext
AI_LANGUAGE_TUTOR/
│── assets/                
│   ├── chat_history.json         # Stores conversation history
│   ├── lesson_plan_inputs.json   # Lesson plan input prompts
│   ├── lesson_plan.json          # Generated lesson plans
│   └── user_vocabulary.json      # Vocabulary list
│
│── pages/                        
│   ├── chatbot.py                # AI chatbot interface
│   ├── history.py                # Lesson history page
│   ├── explain_youtube.py        # Explain YouTube videos
│   ├── lesson_plan.py            # Lesson plan generator
│   └── know_more.py              # Extra topics & resources
│
│── utils/                        
│   ├── config.json               # Configuration settings
│   └── storage.py                # Data saving/loading
│
│── app1.py                       # Main Streamlit entry point
│── sidebar.py                    # Sidebar navigation
│── README.md                     # Documentation
```

---

## ⚙️ Setup & Installation

### **Prerequisites**

* Python **3.8+**
* Valid **Gemini API Key** (stored in environment variables or secure settings)

### **Configuration**

* The AI model and parameters are defined in `utils/config.json`.
* Update the field `gemini_model_name` to switch Gemini models.
* Set the `learning_language` field for personalized learning.

### **Installation**

```sh
# 1. Create a Virtual Environment
python -m venv venv
source venv/bin/activate    # Mac/Linux
venv\Scripts\activate       # Windows

# 2. Install Dependencies
pip install -r requirements.txt

# 3. Run the App
streamlit run app1.py
```

---

## 📖 Usage

1. **Launch the app** with Streamlit.
2. **Start AI conversations** for practice and quizzes.
3. **Generate lesson plans** tailored to your learning goals.
4. **Paste a YouTube link** to get simplified explanations.
5. **Take quizzes** to reinforce learning.
6. **Review past progress** in the lesson history tab.

---

## 📚 References

* [Medium Article – Building an AI-Powered Personal Language Tutor](https://medium.com/@kate.ruksha/building-an-ai-powered-personal-language-tutor-with-chatgpt-59d2e4cd7f56)

---

## ✨ Vision

> *Personalized AI Tutor – making self-paced learning smarter, interactive, and engaging!*
