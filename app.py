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
    try:
        response = requests.get(MESSAGES_URL)
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, list):
            return {"answer": "Error: Unexpected data format from source."}
    except Exception as e:
        return {"answer": f"Error fetching messages: {e}"}

    # Fixed: join strings safely
    all_text = " ".join([msg if isinstance(msg, str) else str(msg) for msg in data])
    q = question.lower()

    try:
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

    except Exception as e:
        return {"answer": f"Error processing your question: {e}"}

    return {"answer": "Sorry, I couldn't find an answer to your question."}

