# AI Interview Coach 

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-green)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-success)

**AI Interview Coach** is an interactive AI-powered web application that simulates technical interviews, evaluates user answers using Large Language Models (LLMs), and provides structured feedback, scoring, and improvement suggestions in real time. 💡📝

---

## Features 

- **Automatic Question Generation**   
  Generates interview questions based on the selected job role.

- **AI Answer Evaluation** 
  Uses reasoning chains to analyze user answers.

- **Structured Feedback Output** 
  - Score (0–10)  
  - Constructive feedback  
  - Ideal / refined answer  
  - Suggestions for improvement   

- **Final Interview Summary**  
  Overall score, strengths, weaknesses, and final advice.

- **User-Friendly Interface**   
  Built with Streamlit for smooth interaction.

- **Powerful Backend** 
  FastAPI-based backend handling all LLM logic and evaluation.

---

## Technologies Used 

- Python  
- Streamlit (Frontend UI)
- FastAPI (Backend API)
- PyTorch & Transformers (LLM inference)
- LangChain (LLM chains & reasoning)
- Pydantic (Data validation)
- ngrok (Expose local backend to public URL)
- Git & GitHub (Version control)

---

## Project Structure 

```text
AI-Interview-Coach/
│
├── app.py                  # Streamlit frontend
├── backend/
│   └── main.ipynb          # FastAPI backend + LLM logic (runs locally)
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation

```
---
## Architecture Overview 

This project uses a **hybrid architecture** to efficiently support heavy AI models while keeping the frontend lightweight and responsive.

### High-Level Design

- The **backend** (FastAPI + LLM inference) runs **locally**.
- **ngrok** exposes the local backend as a secure public HTTPS API.
- The **Streamlit frontend** communicates with the backend using the ngrok URL.

### Request Flow 

1. The user interacts with the Streamlit UI.
2. Streamlit sends requests to the public ngrok API URL.
3. ngrok forwards requests to the local FastAPI backend.
4. The backend runs LLM inference and evaluation logic.
5. Structured results are returned to the frontend.
6. Streamlit displays feedback, scores, and summaries to the user.

---

## How It Works 

### Question Generation 
The backend generates interview questions based on the selected job role using AI models.

### Answer Submission 
Users submit their answers through the Streamlit frontend.

### Evaluation 
Each answer is evaluated using LLM reasoning chains to produce:

- **Score (0–10)** 
- **Constructive feedback**   
- **Ideal / refined answer** 
- **Suggestions for improvement** 

### Summary 
After completing the interview, the backend generates a final summary including overall score, strengths, weaknesses, and final advice.

---

## Getting Started 

### 1️⃣ Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/AI-Interview-Coach.git
cd AI-Interview-Coach
```

#### 2. Install dependencies:
```bash
pip install -r requirements.txt
```

#### 3. Run the backend locally:
```bash
python backend/main.ipynb
```

#### 4. Expose backend using ngrok:
```
ngrok http <PORT>
```
#### 5. Configure the frontend:
In `app.py`, set:
```
API_URL = "https://YOUR_NGROK_URL"
```
#### 6. Run the Streamlit app:
```
streamlit run app.py
```
---

## Deployment
#### Frontend
* Deployed using Streamlit Cloud
* Connected directly to the GitHub repository
* Handles UI and user interaction

#### Backend
* Runs locally due to heavy LLM requirements
* Exposed publicly using ngrok
#### ⚠️ Important:

* ngrok URLs change on every restart (free tier).
* The API_URL in app.py must be updated whenever ngrok restarts.
---

## How It Works 

1. **Question Generation**: The backend (`backend/main.ipynb`) generates interview questions for a selected job role using AI. 
2. **Answer Submission**: Users submit answers through the Streamlit frontend (`app.py`), which sends them to the backend. 
3. **Evaluation**: The backend evaluates each answer using LLM reasoning chains and structured output parsing to provide: 
   - Score (0–10) 
   - Feedback (constructive critique) 
   - Refined/ideal answer 
   - Suggestions for improvement 
4. **Summary**: Once all answers are submitted, the backend generates a portrait summary with overall score, strengths, weaknesses, and final advice. The frontend displays this to the user. 

---

## Notes 

- **Backend**: `backend/main.ipynb` contains all FastAPI routes, LLM inference logic, and evaluation pipeline
- **Frontend** : `app.py` is responsible only for the UI and communication with the backend. 
- **Secuirty**: Do not commit API keys or tokens to the repository.
- **Hardware Requirements**: Large LLM models may require GPU. Running large LLMs on CPU may result in slower response times. 

---
## Future Improvements 

* Dockerized backend deployment
* Persistent backend hosting (no ngrok dependency)
* Session-based user tracking
* Additional job roles and question categories
* Evaluation analytics dashboard 📈

---
## Author 👩‍💻

Built with persistence, patience, and many debugging sessions 😅
Designed to showcase **AI engineering**, **backend design**, and **system architecture skills**.
