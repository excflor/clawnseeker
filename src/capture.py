import mss
import mss.tools
import os
from PIL import Image
from datetime import datetime

class ScreenScanner:
    def __init__(self):
        self.sct = mss.mss()
        # Ensure img directory exists
        if not os.path.exists("img"):
            os.makedirs("img")

    def capture_region(self, x, y, width, height):
        monitor = {"top": y, "left": x, "width": width, "height": height}
        sct_img = self.sct.grab(monitor)
        return Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

    def save_debug_image(self, image):
        # Save with timestamp to track captcha variety
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"img/cap_{timestamp}.png"
        image.save(path)
        return path