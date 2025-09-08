# Personalized AI Tutor

## 📌 Project Overview
Personalized AI Tutor is a AI-powered learning assistant built using **Streamlit** and **Google's Gemini models**. The app provides structured learning with lesson plans, quizzes, and AI-driven conversational practice.

## 🚀 Features
- **AI Chatbot Tutor** – Engage in real-time AI-powered conversations.
- **Lesson Plans** – Auto-generated structured learning plans.
- **Vocabulary Management** – Store, review, and practice new words.
- **Quizzes** – AI-generated quizzes based on stored vocabulary.
- **Lesson History** – Review past conversations and learning progress.

## 🏗️ Tech Stack
- **Frontend:** Streamlit (Fast UI prototyping)
- **Backend:** OpenAI API (LLM-powered tutor)
- **Data Storage:** Local JSON files (User history, vocabulary, lesson plans)
- **Customization:** CSS/HTML for UI enhancements

## 📂 Folder Structure
```plaintext
AI_LANGUAGE_TUTOR/
│── assets/                # Stores user data
│   │── chat_history.json      # Stores conversation history
│   │── lesson_plan_inputs.json  # Inputs for lesson planning
│   │── lesson_plan.json        # Saved lesson plans
│   │── user_vocabulary.json    # User's vocabulary list
│
│── pages/                # Streamlit UI pages
│   │── chatbot.py         # AI chatbot interface
│   │── history.py         # Lesson history page
│   │── lesson_plan.py     # Lesson plan page
│   │── vocab.py           # Vocabulary management page
│
│── utils/                 # Utility functions and configurations
│   │── config.json        # Stores configuration settings
│   │── storage.py         # Handles saving/loading data
│
│── .gitignore             # Ignore unnecessary files
│── app.py                 # Main Streamlit entry point
│── sidebar.py             # Sidebar navigation
│── README.md              # Project documentation
```

## 🛠️ Setup & Installation
### **Configuring the AI Model & Learning Language**
- The AI model and parameters are defined in `utils/config.json`.
- To specify which GPT model to use, update the `openai_model_name` field.
- The learning language can be set in `config.json` under `learning_language`.
- Ensure you provide a valid OpenAI API key in your environment variables or secure settings.


### **Prerequisites**
Ensure you have **Python 3.8+** installed.

### **Installation Steps**
1. **Clone the Repository:**
   ```sh
   git clone https://github.com/your-repo/AI-Language-Tutor.git
   cd AI-Language-Tutor
   ```
2. **Create a Virtual Environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   venv\Scripts\activate     # Windows
   ```
3. **Install Dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Run the App:**
   ```sh
   streamlit run app1.py
   ```

## 📖 Usage Guide
1. **Start the app** and select an activity from the main page.
2. **Use the AI Chat** for practice and quizes
3. **Generate lesson plans** tailored to your learning goals.
5. **Take quizzes** to complete the topic and reinforce learning.
6. **Review past conversations** in the history tab.

## 👨‍💻 Reference
[Medium article](https://medium.com/@kate.ruksha/building-an-ai-powered-personal-language-tutor-with-chatgpt-59d2e4cd7f56).


---
🔹 *Personalized AI tutor - making learning easier!*

