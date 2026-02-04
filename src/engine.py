import interception
import time
import random
import ctypes

class InputEngine:
    def __init__(self):
        try:
            # Set DPI Aware to get actual screen resolution
            try:
                ctypes.windll.shcore.SetProcessDpiAwareness(1)
            except Exception:
                ctypes.windll.user32.SetProcessDPIAware()

            interception.auto_capture_devices(keyboard=True, mouse=True)
            user32 = ctypes.windll.user32
            
            # Use Virtual Screen indices for proper multi-monitor support
            # 76=SM_XVIRTUALSCREEN, 77=SM_YVIRTUALSCREEN, 78=SM_CXVIRTUALSCREEN, 79=SM_CYVIRTUALSCREEN
            self.screen_x = user32.GetSystemMetrics(76)
            self.screen_y = user32.GetSystemMetrics(77)
            self.screen_w = user32.GetSystemMetrics(78)
            self.screen_h = user32.GetSystemMetrics(79)
            
            print(f"DEBUG: Virtual Screen: {self.screen_w}x{self.screen_h} at {self.screen_x},{self.screen_y}")
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

    def move_to(self, x, y):
        # Based on testing, the library likely expects integer pixel coordinates
        # and handles normalization internally or uses a different mode.
        # Sending normalized (large) values caused it to clamp to bottom-right.
        interception.move_to(int(x), int(y))

    def click(self):
        interception.mouse_down("left")
        time.sleep(random.uniform(0.05, 0.1))
        interception.mouse_up("left")