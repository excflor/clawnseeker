import pyautogui

class ScreenScanner:
    def capture_region(self, x, y, width, height):
        try:
            # PyAutoGUI handles the conversion and region bounds internally
            return pyautogui.screenshot(region=(int(x), int(y), int(width), int(height)))
        except Exception as e:
            print(f"🛑 Capture Error: {e}")
            return None

    def check_pixel_color(self, x, y, target_hex="#CC9B12", tolerance=25):
        try:
            # Efficiently convert Hex to RGB tuple
            target = tuple(int(target_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
            current = pyautogui.pixel(int(x), int(y))

            # Use a generator expression for clean, fast tolerance checking
            return all(abs(c - t) <= tolerance for c, t in zip(current, target))
        except Exception:
            return False

    def save_debug_image(self, img, path="debug_capture.png"):
        if img:
            img.save(path)
            return path
        return None