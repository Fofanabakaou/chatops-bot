from pathlib import Path

import httpx
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from bot import answer

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Bonjour"}

@app.get("/ask")
def ask(question: str):
    try:
        reply = answer(question)
    except httpx.HTTPError:
        reply = "Impossible de joindre GitHub pour le moment, réessaie."
    return {"question": question, "answer": reply}

@app.get("/chat", response_class=HTMLResponse)
def chat():
    return (Path(__file__).parent / "chat.html").read_text(encoding="utf-8")







