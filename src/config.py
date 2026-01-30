import json
import os

CONFIG_FILE = "settings.json"

DEFAULT_DATA = {
    "last_selected_map": "default",
    "maps": {
        "default": {"key": "f3", "min_delay": 8.1, "max_delay": 8.7}
    },
    "use_secondary": False,
    "key2": "f4",
    "freq": 4,
    "capture_settings": {
        "x": 815,
        "y": 530,
        "w": 288,
        "h": 70
    }
}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_DATA)
        return DEFAULT_DATA
    
    try:
        with open(CONFIG_FILE, "r") as f:
            user_data = json.load(f)
            
        for key, value in DEFAULT_DATA.items():
            if key not in user_data:
                user_data[key] = value
        return user_data
    
    except (json.JSONDecodeError, IOError):
        return DEFAULT_DATA

def save_config(full_data):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(full_data, f, indent=4)
    except Exception as e:
        print(f"🛑 Critical: Failed to save config: {e}")