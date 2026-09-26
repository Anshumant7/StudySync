import json
import os

USERS_FILE = "data/users.json"
TASKS_FILE = "data/tasks.json"

def load_json(file_path):
    if not os.path.exists(file_path):
        if file_path == USERS_FILE:
            return {}
        return []

    with open(file_path, "r") as f:
        return json.load(f)

def save_json(file_path, data):
    folder = os.path.dirname(file_path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)