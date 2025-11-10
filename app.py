# app.py
from fastapi import FastAPI, Query
import requests
import re

# URL of the public messages API
MESSAGES_URL = "https://november7-730026606190.europe-west1.run.app/messages"

# Initialize FastAPI app
app = FastAPI()

# Root endpoint
@app.get("/")
def home():
    return {"message": "Welcome to the Member Q&A API! Use /ask?question=..."}

# Question-answering endpoint
@app.get("/ask")
def ask(question: str = Query(..., description="Natural language question")):
    try:
        # Fetch messages from the public API
        response = requests.get(MESSAGES_URL)
        response.raise_for_status()
        data = response.json()
        # Extract 'messages' from the API response
        messages = data.get("messages", [])
        if not isinstance(messages, list):
            return {"answer": "Error: Unexpected messages format."}
    except Exception as e:
        return {"answer": f"Error fetching messages: {e}"}

    # Combine all message texts into a single string
    all_text = " ".join([msg.get("message", "") for msg in messages])
    q = question.lower()

    try:
        # Match trip-related questions
        if "trip" in q and ("when" in q or "date" in q):
            match = re.search(r"(\w+)\s.*trip.*to\s(\w+).*?(\d{4}-\d{2}-\d{2})", all_text)
            if match:
                name, place, date = match.groups()
                return {"answer": f"{name} is planning a trip to {place} on {date}."}

        # Match car-related questions
        if "car" in q and "how many" in q:
            match = re.search(r"(\w+)\s.*has\s(\d+)\scars?", all_text)
            if match:
                name, count = match.groups()
                return {"answer": f"{name} has {count} cars."}

        # Match favorite restaurant questions
        if "favorite" in q and "restaurant" in q:
            match = re.search(r"(\w+).*favorite restaurants? are (.+?)\.", all_text)
            if match:
                name, restaurants = match.groups()
                return {"answer": f"{name}'s favorite restaurants are {restaurants}."}

    except Exception as e:
        return {"answer": f"Error processing your question: {e}"}

    # If no match found
    return {"answer": "Sorry, I couldn't find an answer to your question."}
