import interception
import time
import random

class InputEngine:
    def __init__(self):
        try:
            interception.auto_capture_devices(keyboard=True)
        except Exception as e:
            print(f"Driver Error: {e}")

    def simulate_press(self, key_name, min_delay, max_delay):
        # Press
        interception.key_down(key_name)
        time.sleep(random.uniform(0.05, 0.12))
        interception.key_up(key_name)
        
        # Calculate delay
        actual_delay = random.uniform(min_delay, max_delay)
        time.sleep(max(0.01, actual_delay))
        
        # Return milliseconds for the log window
        return int(actual_delay * 1000)