import json
import os

CONFIG_FILE = "settings.json"

# Default profiles if no file exists
DEFAULT_DATA = {
    "last_selected_map": "verdandi",
    "maps": {
        "verdandi": {"key": "f3", "min_delay": 8.0, "max_delay": 9.0},
        "asgard": {"key": "f1", "min_delay": 5.0, "max_delay": 6.0}
    },
    "secondary": {
        "use_secondary": False,
        "key2": "f4",
        "freq": 4
    },
    "capture_settings": {
        "x": 815,
        "y": 530,
        "w": 288,
        "h": 70
    }
}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return DEFAULT_DATA
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except:
        return DEFAULT_DATA

def save_config(full_data):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(full_data, f, indent=4)
    except Exception as e:
        print(f"Failed to save config: {e}")