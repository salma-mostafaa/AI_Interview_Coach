# AI Interview Coach 🚀🤖

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-green)

**AI Interview Coach** is an interactive web application that simulates technical interviews, evaluates user answers using Large Language Models (LLMs), and provides structured feedback, scoring, and improvement suggestions in real-time. 💡📝


---

## Features ✨

- **Automatic Question Generation**: Generates interview questions based on the selected job role.🧠
- **Answer Evaluation**: Uses AI reasoning chains to assess answers.📊
- **Structured Output Parsing** 🗂️:
  - Score (0–10) 
  - Constructive feedback 
  - Ideal/refined answer 
  - Suggestions for improvement 🔧
- **Summary Evaluation**: Provides an overall score, strengths, weaknesses, and final advice.📋
- **User-Friendly Interface**: Built with Streamlit for easy interaction.🖥️
- **Backend Notebook**: `backend/main.ipynb` contains the core backend logic and FastAPI routes.📚

---


## Technologies Used 🛠️

- Python
- Streamlit (Frontend & Deployment)
- FastAPI (Backend API and evaluation)
- PyTorch & Transformers (LLM inference)
- LangChain (Chains for structured evaluation)
- Pydantic (Data validation)
- Git + GitHub (Version control)
- Streamlit Cloud (Deployment)

---

## Project Structure 📂

```text
AI-Interview-Coach/
│
├── app.py                 # Streamlit frontend application 
├── backend/
│   └── main.ipynb         # Notebook for backend logic and LLM evaluation routes  
├── requirements.txt       # Python dependencies 
└── README.md              # This file 


```
---

## Getting Started 🚀

#### 1. Clone the repository:
```
git clone https://github.com/YOUR_USERNAME/AI-Interview-Coach.git
cd AI-Interview-Coach
```

#### 2. Install dependencies:
```
pip install -r requirements.txt
```

#### 3. Run the Streamlit app:
```
streamlit run app.py
```

#### 4. Open the URL provided by Streamlit in your browser to start the interview. 🌐

---

## Deployment

The project is deployed using **Streamlit Cloud**:

* 🔗 Connects directly to the GitHub repository.
* 📦 Automatically installs dependencies from requirements.txt.
* 🌍 Provides a publicly accessible web interface.
* 📝 Users can select a job role, answer questions, and receive AI-generated evaluation in real-time.

---
## How It Works 🧩

1. **Question Generation**: The backend (`backend/main.ipynb`) generates interview questions for a selected job role using AI. 🤔
2. **Answer Submission**: Users submit answers through the Streamlit frontend (`app.py`), which sends them to the backend. 📝
3. **Evaluation**: The backend evaluates each answer using LLM reasoning chains and structured output parsing to provide: 📊
   - Score (0–10) 🏆
   - Feedback (constructive critique) ✍️
   - Refined/ideal answer 💯
   - Suggestions for improvement 🔧
4. **Summary**: Once all answers are submitted, the backend generates a portrait summary with overall score, strengths, weaknesses, and final advice. The frontend displays this to the user. 📋

---

## Notes ⚠️

- **Backend**: `backend/main.ipynb` contains the FastAPI routes, evaluation logic, and all LLM-based processing. It is the core backend of the project. 🖥️
- **Frontend** : `app.py` is the Streamlit interface that interacts with the backend and displays questions, collects answers, and shows evaluation results. 🖥️
- **Environment Variables**: Do not include API keys or tokens in the repo; store them securely.🔒
- **Hardware Requirements**: Large LLM models may require GPU. Streamlit Cloud may use CPU, which can make responses slower. 🖥️

