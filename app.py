# app.py
from fastapi import FastAPI, Query
import requests
import re

app = FastAPI(title="Member Question Answering API")

MESSAGES_URL = "https://november7-730026606190.europe-west1.run.app/messages"

@app.get("/")
def home():
    return {"message": "Welcome to the Member Q&A API! Use /ask?question=..."}

@app.get("/ask")
def ask(question: str = Query(..., description="Natural language question")):
    response = requests.get(MESSAGES_URL)
    if response.status_code != 200:
        return {"answer": "Error fetching data from source."}
    data = response.json()

    all_text = " ".join([msg.get("message", "") for msg in data])
    q = question.lower()

    # --- Rule-based pattern examples ---
    if "trip" in q and ("when" in q or "date" in q):
        match = re.search(r"(\w+)\s.*trip.*to\s(\w+).*?(\d{4}-\d{2}-\d{2})", all_text)
        if match:
            name, place, date = match.groups()
            return {"answer": f"{name} is planning a trip to {place} on {date}."}

    if "car" in q and "how many" in q:
        match = re.search(r"(\w+)\s.*has\s(\d+)\scars?", all_text)
        if match:
            name, count = match.groups()
            return {"answer": f"{name} has {count} cars."}

    if "favorite" in q and "restaurant" in q:
        match = re.search(r"(\w+).*favorite restaurants? are (.+?)\.", all_text)
        if match:
            name, restaurants = match.groups()
            return {"answer": f"{name}'s favorite restaurants are {restaurants}."}

    return {"answer": "Sorry, I couldn't find an answer to your question."}
