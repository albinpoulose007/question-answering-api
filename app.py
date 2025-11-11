from fastapi import FastAPI, Query
import requests
import re

app = FastAPI(title="Member Q&A API")

# Public API URL with member messages
MESSAGES_URL = "https://november7-730026606190.europe-west1.run.app/messages"

@app.get("/")
def home():
    return {"message": "Welcome to the Member Q&A API! Use /ask?question=..."}

@app.get("/ask")
def ask(question: str = Query(..., description="Ask a natural language question")):
    """
    Handles questions like:
    - When is Layla planning her trip to London?
    - How many cars does Vikram Desai have?
    - What are Amira's favorite restaurants?
    """
    try:
        response = requests.get(MESSAGES_URL)
        response.raise_for_status()
        data = response.json()
        messages = data.get("messages", [])
        if not isinstance(messages, list):
            return {"answer": "Error: Unexpected data format."}
    except Exception as e:
        return {"answer": f"Error fetching messages: {e}"}

    # Combine all messages into one big searchable string
    all_text = " ".join([msg.get("message", "") for msg in messages])
    q = question.lower()

    # --- Extract functions ---

    def extract_trip():
        # Match: "Layla is planning a trip to London on 2025-11-20"
        match = re.search(
            r"([A-Z][a-z]+(?:\s[A-Z][a-z]+)*) .*?trip.*?to ([A-Z][a-z]+(?:\s[A-Z][a-z]+)*) .*?(\d{4}-\d{2}-\d{2})",
            all_text,
            re.IGNORECASE
        )
        if match:
            name, place, date = match.groups()
            return f"{name} is planning a trip to {place} on {date}."
        return None

    def extract_car():
        # Match: "Vikram Desai has 2 cars"
        match = re.search(
            r"([A-Z][a-z]+(?:\s[A-Z][a-z]+)*) .*?has (\d+) cars?",
            all_text,
            re.IGNORECASE
        )
        if match:
            name, count = match.groups()
            return f"{name} has {count} cars."
        return None

    def extract_restaurant():
        # Match: "Amira’s favorite restaurants are Sushi Palace and Tandoori Grill."
        match = re.search(
            r"([A-Z][a-z]+).*?favorite restaurants? (?:are|include) (.+?)(?:\.|$)",
            all_text,
            re.IGNORECASE
        )
        if match:
            name, restaurants = match.groups()
            return f"{name}'s favorite restaurants are {restaurants}."
        return None

    # --- Select extraction based on question ---
    answer = None
    if "trip" in q or "travel" in q:
        answer = extract_trip()
    if not answer and "car" in q:
        answer = extract_car()
    if not answer and "restaurant" in q:
        answer = extract_restaurant()

    # Fallback
    if not answer:
        answer = "Sorry, I couldn't find an answer to your question."

    return {"answer": answer}
