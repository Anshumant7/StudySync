from datetime import datetime

PRIORITY_LEVELS = ["low", "medium", "high"]
PRIORITY_WEIGHT = {"low": 1, "medium": 2, "high": 3}


def is_valid_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def is_valid_priority(priority_text):
    return priority_text.lower() in PRIORITY_LEVELS

def is_valid_hours(hours_text):
    try:
        hours = float(hours_text)
    except ValueError:
        return False
    return hours > 0

def days_between(today_text, due_text):
    today = datetime.strptime(today_text, "%Y-%m-%d")
    due = datetime.strptime(due_text, "%Y-%m-%d")
    return (due - today).days