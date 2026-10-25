from fastapi import FastAPI

from bot import answer

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Bonjour"}


@app.get("/ask")
def ask(question: str):
    return {"question": question, "answer": answer(question)}
