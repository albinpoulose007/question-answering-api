import re

def extract_trip_answer(all_text):
    # Match: "<Name> ... trip ... to <Place> ... <date>"
    match = re.search(
        r"([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)\s.*?trip.*?to\s([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)\s.*?(\d{4}-\d{2}-\d{2})",
        all_text,
        re.IGNORECASE
    )
    if match:
        name, place, date = match.groups()
        return f"{name} is planning a trip to {place} on {date}."
    return None

def extract_car_answer(all_text):
    match = re.search(
        r"([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)\s.*?has\s(\d+)\s?cars?",
        all_text,
        re.IGNORECASE
    )
    if match:
        name, count = match.groups()
        return f"{name} has {count} cars."
    return None

def extract_restaurant_answer(all_text):
    match = re.search(
        r"([A-Z][a-z]+).*?favorite restaurants? (?:are|include) (.+?)(?:\.|$)",
        all_text,
        re.IGNORECASE
    )
    if match:
        name, restaurants = match.groups()
        return f"{name}'s favorite restaurants are {restaurants}."
    return None
