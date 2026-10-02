from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0"
)


# Static files
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# HTML templates
templates = Jinja2Templates(
    directory="templates"
)


# Home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "result": None,
            "task": None,
            "input_text": ""
        }
    )


# Main processing route
@app.post("/process", response_class=HTMLResponse)
async def process_request(
    request: Request,
    task: str = Form(...),
    input_text: str = Form(...)
):

    result = None

    if task == "qa":
        result = answer_question(input_text)

    elif task == "explain":
        result = explain_topic(input_text)

    elif task == "quiz":
        result = generate_quiz(input_text)

    elif task == "summarize":
        result = summarize_text(input_text)

    elif task == "recommend":
        result = get_learning_recommendations(input_text)

    else:
        result = "Invalid task selected."

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "result": result,
            "task": task,
            "input_text": input_text
        }
    )


# Q&A API endpoint
@app.post("/qa")
async def qa_endpoint(
    question: str = Form(...)
):
    return {
        "answer": answer_question(question)
    }


# Explanation API endpoint
@app.post("/explain")
async def explain_endpoint(
    topic: str = Form(...)
):
    return {
        "explanation": explain_topic(topic)
    }


# Quiz API endpoint
@app.post("/quiz")
async def quiz_endpoint(
    text: str = Form(...)
):
    return {
        "quiz": generate_quiz(text)
    }


# Summary API endpoint
@app.post("/summarize")
async def summarize_endpoint(
    text: str = Form(...)
):
    return {
        "summary": summarize_text(text)
    }


# Learning path API endpoint
@app.post("/learn/recommendations")
async def learning_path_endpoint(
    topic: str = Form(...)
):
    return {
        "recommendations": get_learning_recommendations(topic)
    }


# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "running",
        "application": "EduGenie"
    }