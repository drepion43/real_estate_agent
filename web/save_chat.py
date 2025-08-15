import os
import json

DATA_DIR = "/home/data/real_estate_agent/web/chat_data"

def get_user_file(login_user):
    os.makedirs(DATA_DIR, exist_ok=True)
    return os.path.join(DATA_DIR, f"{login_user}.json")

def save_user_data(login_user, user_data):
    file = get_user_file(login_user)
    with open(file, "w", encoding="utf-8") as f:
        json.dump(user_data, f, ensure_ascii=False)

def load_user_data(login_user):
    file = get_user_file(login_user)
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    
    return {
        "openai_api_key": None,
        "threads": {},
        "current_thread": None,
        "delete_thread": None
    }