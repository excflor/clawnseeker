import pyautogui
from PIL import Image
import numpy as np

class ScreenScanner:
    def __init__(self):
        pass

    def capture_region(self, x, y, width, height):
        try:
            img = pyautogui.screenshot(region=(int(x), int(y), int(width), int(height)))
            return img
        except Exception as e:
            print(f"🛑 Capture Failed: {e}")
            return None

    def check_pixel_color(self, x, y, target_hex="#CC9B12", tolerance=25):
        try:
            # Convert hex to RGB
            h = target_hex.lstrip('#')
            target_rgb = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
            
            # Get the actual pixel RGB
            current_rgb = pyautogui.pixel(int(x), int(y))
            
            # Calculate if color matches within tolerance
            match = all(abs(current_rgb[i] - target_rgb[i]) <= tolerance for i in range(3))
            return match
        except Exception:
            return False

    def save_debug_image(self, img):
        if img:
            path = "debug_capture.png"
            img.save(path)
            return path
        return None