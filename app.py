import streamlit as st
import requests
import time

# ----------------- CONFIG ----------------- 
API_URL = "https://YOUR_NGROK_URL"

# ----------------- PAGE SETUP -----------------
st.set_page_config(page_title="AI Interview Coach", layout="wide", initial_sidebar_state="collapsed")

# ----------------- CSS STYLING -----------------

st.markdown("""

    <style>
    /* 1. GLOBAL OVERRIDES & BACKGROUND */
    header {visibility: hidden;}
    .main .block-container {padding-top: 2rem;}

    .stApp {
       background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)),
                    url("https://i.pinimg.com/1200x/f2/68/7a/f2687adc1bdca1c79177592bc148b3ab.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }

    /* 2. TYPOGRAPHY */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown p, .stMarkdown li, span {
        color: white !important;
    }


    label, .stWidgetFormLabel, .stSlider p {
        color: white !important;
        font-weight: 500 !important;
    }

    /* 3. INPUTS & SELECTBOXES */
    div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(0, 128, 128, 0.3) !important;
    }

    div[data-baseweb="select"] span, div[data-baseweb="select"] div {
        color: white !important;
    }

    /* 4. TOTAL TRANSPARENCY FOR STATUS & LOADING */
    div[data-testid="stStatusContainer"],
    div[data-testid="stStatusContainer"] > div,

    .stStatus {
        background-color: rgba(0, 0, 0, 0.4) !important;
        border: 1px solid rgba(0, 128, 128, 0.4) !important;
        color: white !important;
    }
    div[data-testid="stSkeleton"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        background-image: none !important;
        border-radius: 8px;
    }
            
    /* 5. CARDS & EXPANDERS */
    div[data-testid="stExpander"] {
        background-color: rgba(0, 0, 0, 0.4) !important;
        border: 1px solid rgba(0, 128, 128, 0.4) !important;
        border-radius: 8px;
        backdrop-filter: blur(5px);
    }

    div[data-testid="stExpander"] details {
        background-color: transparent !important;
    }

    div[data-testid="stExpander"] summary {
        background-color: transparent !important;
        color: white !important;
    }



    /* 6. BUTTONS */
    .stButton>button {
        background-color: #0D212D !important;
        color: white !important;
        border: 1px solid rgba(0, 128, 128, 0.5) !important;
        border-radius: 8px;
        transition: all 0.3s ease-in-out;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
    }
            
    .stButton>button:hover {
        background-color: white !important;
        color: #0D212D !important;
        border-color: white !important;
    }
            
    .stButton>button:hover p, .stButton>button:hover span {
        color: #0D212D !important;
    }
            
    /* 7. PROGRESS & CIRCLES */
    .score-circle {
        background: rgba(79, 209, 197, 0.1);
        border: 2px solid #4fd1c5;
        border-radius: 50%;
        width: 80px;
        height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        font-weight: bold;
        color: #4fd1c5;
        margin: 0 auto;
    }
            
    .stProgress > div > div > div > div {
        background-color: #4fd1c5 !important;
    }

    /* 8. FIX: FORCE TRANSPARENCY ON INFO/SUCCESS (Blue/Green boxes) */
    /* We target the specific ARIA role and data-testid that Streamlit uses for colors */
    div[data-testid="stNotification"], div[role="alert"] {
        background-color: rgba(255, 255, 255, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
    }

    /* Force all nested text elements inside those boxes to be white */
    div[data-testid="stNotification"] p,
    div[data-testid="stNotification"] div,
    div[data-testid="stNotification"] span {
        color: white !important;
    }

    /* Fix icons in notifications */
    div[data-testid="stNotification"] svg {
        fill: white !important;
        color: white !important;

    }
    </style>

    """, unsafe_allow_html=True)

# ----------------- SESSION STATE -----------------
if "session_id" not in st.session_state:
    st.session_state.update({
        "session_id": None,
        "questions": [],
        "current_index": 0,
        "completed": False,
        "evaluation_results": None,
        "summary": None,
        "job_title": ""
    })

job_roles = [
    "Software Engineer", "Frontend Developer", "Backend Developer",
    "Full Stack Developer", "AI Engineer", "Data Scientist",
    "Machine Learning Engineer", "Data Analyst", "Data Engineer",
    "DevOps Engineer", "Cloud Architect", "Cybersecurity Analyst",
    "Mobile App Developer", "Game Developer", "UI/UX Designer",
    "Product Manager", "QA Automation Engineer", "Embedded Systems Engineer",
    "Site Reliability Engineer (SRE)", "System Administrator"
]

# ----------------- STEP 1: INTERVIEW SETUP -----------------
if not st.session_state.session_id:
    st.title("🤖 Next Round")
    st.write("Next Round is a AI Interview Coach to help you Sharpen your skills with AI-driven technical mock interviews.")

    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            job = st.selectbox("Target Role", job_roles)
        with col2:
            num_q = st.slider("Number of Questions", 2, 5, 4)

        if st.button("Start Interview", use_container_width=True):
            with st.status("Initializing AI Interviewer...", expanded=True) as status:
                try:
                    res = requests.post(f"{API_URL}/start", json={"job_title": job, "num_questions": num_q})
                    if res.status_code == 200:
                        data = res.json()
                        st.session_state.session_id = data["session_id"]
                        st.session_state.questions = data["questions"]
                        st.session_state.job_title = job
                        status.update(label="Questions Ready!", state="complete", expanded=False)
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Backend Error")
                except Exception as e:
                    st.error(f"Connection Failed: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

# ----------------- STEP 2: THE INTERVIEW -----------------
elif not st.session_state.completed:
    idx = st.session_state.current_index
    qs = st.session_state.questions

    st.title(f"Question {idx + 1} of {len(qs)}")
    st.progress((idx) / len(qs))

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader(qs[idx])

    answer_input = st.text_area(
        "Your Response",
        placeholder="Explain your thought process...",
        height=250,
        key=f"user_answer_input_{idx}"
    )

    if st.button("Submit Answer", use_container_width=True):
        if not answer_input.strip():
            st.warning("⚠️ Please provide an answer before submitting.")
        else:
            with st.spinner("🚀 AI is recording your response..."):
                try:
                    payload = {
                        "session_id": str(st.session_state.session_id),
                        "answer": str(answer_input)
                    }
                    res = requests.post(f"{API_URL}/submit", json=payload)
                    if res.status_code == 200:
                        if idx + 1 < len(qs):
                            st.session_state.current_index += 1
                        else:
                            st.session_state.completed = True
                        st.rerun()
                    else:
                        st.error(f"Failed to save: {res.status_code} - {res.text}")
                except Exception as e:
                    st.error(f"Connection Error: {str(e)}")

    st.markdown('</div>', unsafe_allow_html=True)

# ----------------- STEP 3 & 4: EVALUATION -----------------
else:
    st.title("🎯 Performance Analysis")

    if not st.session_state.evaluation_results:
        with st.status("Analyzing your performance...", expanded=True) as status:
            try:
                eval_res = requests.post(f"{API_URL}/evaluate", json={"session_id": st.session_state.session_id})
                sum_res = requests.post(f"{API_URL}/summary", json={"session_id": st.session_state.session_id})

                if eval_res.status_code == 200 and sum_res.status_code == 200:
                    results = eval_res.json().get("results", [])
                    summary = sum_res.json()
                    if results:
                        st.session_state.evaluation_results = results
                        st.session_state.summary = summary
                        status.update(label="Analysis Complete!", state="complete", expanded=False)
                        st.rerun()
                    else:
                        st.error("Evaluation returned no results. Please make sure you answered all questions.")
                else:
                    st.error(f"Failed to fetch evaluation. Status codes: eval={eval_res.status_code}, summary={sum_res.status_code}")
            except Exception as e:
                st.error(f"Analysis interrupted: {e}")

    if st.session_state.evaluation_results:
        st.markdown("### 🔍 Question-by-Question Breakdown")
        for i, item in enumerate(st.session_state.evaluation_results):
            score = int(item.get('score', 0))
            color = "#4fd1c5" if score >= 8 else "#f6ad55" if score >= 4 else "#fc8181"

            st.markdown(f'<div class="glass-card" style="border-left: 5px solid {color};">', unsafe_allow_html=True)
            st.markdown(f"#### Q{i+1}: {item.get('question', 'No question available')}")

            col_left, col_right = st.columns(2)
            with col_left:
                st.markdown("**👤 Your Answer**")
                st.info(item.get('answer', 'No answer available'))
                st.markdown(f"**Score:** <span style='color:{color}; font-weight:bold; font-size:1.2rem;'>{score}/10</span>", unsafe_allow_html=True)

            with col_right:
                st.markdown("**🏆 Refined Answer**")
                st.success(item.get('refined_answer') or "N/A")

            with st.expander("💡 Critique & Suggestions"):
                st.write(f"**Feedback:** {item.get('feedback', 'No feedback.')}")
                st.write(f"**Improvement Points:** {item.get('suggestions', 'No suggestions.')}")
            st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.summary:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.header("🏁 Final Verdict")
        s = st.session_state.summary
        eval_scores = [int(item.get('score', 0)) for item in st.session_state.evaluation_results]
        real_score = int((sum(eval_scores) / (len(eval_scores) * 10)) * 100) if eval_scores else 0

        c1, c2, c3 = st.columns([1, 2, 2])
        with c1:
            st.markdown(f'<div class="score-circle">{real_score}%</div>', unsafe_allow_html=True)
            st.markdown("<p style='text-align:center;'>Total Readiness</p>", unsafe_allow_html=True)
        with c2:
            st.write("**💪 Key Strengths**")
            strengths = s.get("strengths", [])
            for strength in strengths:
                st.write(f"✅ {strength}")
        with c3:
            st.write("**🎯 Growth Areas**")
            weaknesses = s.get("weaknesses", [])
            for weakness in weaknesses:
                st.write(f"🚩 {weakness}")

        st.divider()
        st.write(f"**Coach's Advice:** {s.get('final_advice', 'Keep practicing!')}")

        if st.button("Start New Session", use_container_width=True):
            st.session_state.clear()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
