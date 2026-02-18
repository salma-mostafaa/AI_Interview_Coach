import json
import uuid
import random
import re
import asyncio
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from langchain_core.output_parsers import ResponseSchema, StructuredOutputParser


# ---------------------MODEL_CONFIG---------------------------


MODEL_NAME = "mistralai/Mistral-Nemo-Instruct-2407"

quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True
)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME, 
    quantization_config=quant_config,
    device_map="auto"
)


# ---------------------SCHEMAS---------------------------

single_eval_schema = [
    ResponseSchema(name="score", description="An integer from 0-10."),
    ResponseSchema(name="feedback", description="Constructive critique of the user's answer."),
    ResponseSchema(name="refined_answer", description="The 'Ideal' version of the answer the user should have given."),
    ResponseSchema(name="suggestions", description="Bullet points on technical keywords or concepts to add.")
]
single_parser = StructuredOutputParser.from_response_schemas(single_eval_schema)

summary_schema = [
    ResponseSchema(name="overall_score", description="0-100 total readiness."),
    ResponseSchema(name="strengths", description="List of strings of user strengths."),
    ResponseSchema(name="weaknesses", description="List of strings of user weaknesses."),
    ResponseSchema(name="final_advice", description="A motivating final paragraph.")
]
summary_parser = StructuredOutputParser.from_response_schemas(summary_schema)




# ---------------------LOGIC---------------------------

SESSIONS = {}

def extract_questions(text: str):
    """Try to extract a JSON list of questions from the LLM output."""
    if not text:
        return None

    text = re.sub(r"```json|```", "", text, flags=re.IGNORECASE)

    list_match = re.search(r"\[[\s\S]*?\]", text)
    if list_match:
        try:
            data = json.loads(list_match.group())
            if isinstance(data, list):
                return data
        except json.JSONDecodeError:
            pass

    obj_match = re.search(r"\{[\s\S]*?\}", text)
    if obj_match:
        try:
            data = json.loads(obj_match.group())
            if isinstance(data, dict) and "questions" in data:
                return data["questions"]
        except json.JSONDecodeError:
            pass

    return None


def is_meaningful(text: str) -> bool:
    clean = text.strip().lower()
    if len(clean) < 5:
        return False
    words = clean.split()
    if len(words) < 2:
        return False
    if len(clean) > 12 and not any(v in clean for v in "aeiou"):
        return False
    return True


async def run_llm_task(prompt: str, max_tokens: int, temp: float = 0.0):
    loop = asyncio.get_event_loop()

    def generate():
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        with torch.inference_mode():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temp,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id
            )
        return tokenizer.decode(
            outputs[0][inputs.input_ids.shape[1]:],
            skip_special_tokens=True
        ).strip()

    return await loop.run_in_executor(None, generate)


# ---------------------START_INTERVIEW---------------------------


async def start_interview(job_title: str, num_questions: int):
    session_id = str(uuid.uuid4())
    num_tech = num_questions // 2
    num_soft = num_questions - num_tech
    job_subtopics = {
        "Software Engineer": ["system architecture", "scalability", "debugging", "API design"],
        "Frontend Developer": ["UI design", "responsive layout", "frontend performance", "state management"],
        "Backend Developer": ["API design", "database design", "scalability", "security"],
        "Full Stack Developer": ["API design", "UI/UX", "database design", "system architecture"],
        "AI Engineer": ["model deployment", "data pipelines", "scalability", "ML systems"],
        "Data Scientist": ["statistics", "data analysis", "ML models", "feature engineering"],
        "Machine Learning Engineer": ["model optimization", "deployment", "scalability", "data preprocessing"],
        "Data Analyst": ["SQL", "data visualization", "ETL", "business insights"],
        "Data Engineer": ["ETL pipelines", "data warehousing", "scalability", "cloud data systems"],
        "DevOps Engineer": ["CI/CD", "monitoring", "infrastructure as code", "cloud systems"],
        "Cloud Architect": ["cloud design", "scalability", "security", "cost optimization"],
        "Cybersecurity Analyst": ["threat detection", "network security", "incident response"],
        "Mobile App Developer": ["mobile architecture", "performance optimization", "UI/UX"],
        "Game Developer": ["game loops", "performance optimization", "graphics systems"],
        "UI/UX Designer": ["design systems", "user research", "prototyping"],
        "Product Manager": ["requirements analysis", "roadmaps", "stakeholder communication"],
        "QA Automation Engineer": ["test automation", "CI/CD testing", "bug tracking"],
        "Embedded Systems Engineer": ["real-time systems", "hardware interfacing", "low-level programming"],
        "Site Reliability Engineer (SRE)": ["monitoring", "incident response", "scalability"],
        "System Administrator": ["server management", "networking", "security"]
    }

    random_focus = random.choice(job_subtopics.get(job_title, ["system architecture", "scalability", "debugging", "API design"]))

    prompt = f"""<s>[INST] <<SYS>> Return ONLY a JSON list of strings. <</SYS>>
Generate {num_questions} interview questions for a {job_title}.
- {num_tech} Technical ({random_focus})
- {num_soft} Soft skills. [/INST]"""

    gen_text = await run_llm_task(prompt, max_tokens=600)
    final_qs = extract_questions(gen_text)

    if not final_qs:
        final_qs = ["Tell me about your background."]
    final_qs = final_qs[:num_questions]

    answers = [""] * len(final_qs)

    SESSIONS[session_id] = {
        "job_title": job_title,
        "questions": final_qs,
        "answers": answers,
        "results": []
    }

    return {"session_id": session_id, "questions": final_qs}


# ---------------------SUBMIT---------------------------


def submit_answer(session_id:str, answer:str):
    session = SESSIONS.get(session_id)
    if not session:
        return {"error": "Session not found."}

    try:
        idx = session["answers"].index("")
        session["answers"][idx] = answer
    except ValueError:
        return {"completed": True}

    completed = all(is_meaningful(a) or a == "" for a in session["answers"])
    return {"completed": completed}


# ---------------------EVALUATE---------------------------

async def evaluate(session_id: str):
    session = SESSIONS.get(session_id)
    if not session:
        return {"error": "Invalid session"}

    questions = session.get("questions", [])
    answers = session.get("answers", [])
    format_instructions = single_parser.get_format_instructions()

    eval_template = """<s>[INST]
You are a strict Technical Hiring Manager evaluating a candidate for a {role} position.

RULES (MANDATORY):
- If answer is gibberish or meaningless, score MUST be 0–2

SCORING RUBRIC:
- 0–2: Empty, gibberish, irrelevant
- 3–5: Partially correct, lacks depth
- 6–8: Correct with solid understanding
- 9–10: Exceptional; edge cases, trade-offs, best practices

DEFINITIONS:
- feedback: Critical and honest evaluation
- refined_answer: High-quality model answer
- suggestions: Missing keywords or improvements

{format_instructions}

QUESTION:
{q}

CANDIDATE ANSWER:
{a}

IMPORTANT INSTRUCTION:
- If the candidate answer is gibberish, unreadable, or extremely brief, still generate a high-quality model answer in "refined_answer".
- Provide critical and honest "feedback".
- Provide "suggestions" for improvement.
- Score must be 0–2 if the answer is gibberish.
[/INST]"""

    async def evaluate_one(q, a):
        meaningful = is_meaningful(a)

        prompt = eval_template.format(
            role=session.get("job_title", "Unknown Role"),
            q=q,
            a=a if meaningful else "[Candidate answer is gibberish]",
            format_instructions=format_instructions
        )

        raw_gen = await run_llm_task(prompt, max_tokens=450, temp=0.0)
        
        try:
            parsed = single_parser.parse(raw_gen)
        except Exception:
            parsed = {
        "score": 0,
        "feedback": "Failed to parse",
        "refined_answer": "N/A",
        "suggestions": "N/A"
    }

        if not parsed:
            parsed = {"score": 0, "feedback": "Failed to parse", "refined_answer": "N/A", "suggestions": "N/A"}

        if not meaningful:
            parsed["score"] = min(parsed.get("score", 0), 2)
            parsed["feedback"] = "Response detected as gibberish or too brief to evaluate."

        parsed.update({"question": q, "answer": a})
        return parsed

    tasks = [evaluate_one(q, a) for q, a in zip(questions, answers)]
    results = await asyncio.gather(*tasks)
    session["results"] = results
    torch.cuda.empty_cache()
    return {"results": results}


# ---------------------SUMMARY---------------------------

async def summary(session_id: str):
    session = SESSIONS.get(session_id)
    if not session or not session.get("answers"):
        return {"overall_score": 0, "strengths": [], "weaknesses": [], "final_advice": "No answers submitted."}

    format_instructions = summary_parser.get_format_instructions()

    context_list = [f"Q: {q} | A: {a}" for q, a in zip(session["questions"], session["answers"])]
    data_str = "\n".join(context_list)

    summary_template = """<s>[INST] You are a strict senior career coach. 
Evaluate the interview performance for a {job_title} role **strictly based on the candidate's actual answers**. 

{format_instructions}

PERFORMANCE DATA:
{data_str}

Instructions:
1. Assign an "overall_score" 0-100 strictly based on quality, clarity, and technical correctness.
2. List up to 3 **real strengths**. If none, return an empty list [].
3. List up to 3 **real weaknesses**. If none, return an empty list [].
4. Provide "final_advice" in exactly 2 sentences, grounded in the candidate’s actual answers.
5. Do NOT make up skills, examples, or scenarios. If answers are unreadable or irrelevant, indicate that clearly.
[/INST]"""

    prompt = summary_template.format(
        job_title=session['job_title'],
        data_str=data_str,
        format_instructions=format_instructions
    )

    raw_output = await run_llm_task(prompt, max_tokens=300, temp=0.3)
    
    try:
        parsed_sum = summary_parser.parse(raw_output)
    except Exception:
        parsed_sum = {
        "overall_score": 0,
        "strengths": [],
        "weaknesses": ["Error parsing summary"],
        "final_advice": "Summary failed."
    }

    if not parsed_sum:
        return {"overall_score": 0, "strengths": [], "weaknesses": ["Error"], "final_advice": "Summary failed."}

    return parsed_sum
