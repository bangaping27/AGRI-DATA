import json
import os
from config import PROGRESS_FILE

def load_progress():
    if not os.path.exists(PROGRESS_FILE):
        return {}
        
    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_progress(province, district, subdistrict):
    state_dir = os.path.dirname(PROGRESS_FILE)
    if not os.path.exists(state_dir) and state_dir != '':
        os.makedirs(state_dir)
        
    state = {
        "province": province,
        "district": district,
        "subdistrict": subdistrict
    }
    
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=4)

def reset_progress():
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)
