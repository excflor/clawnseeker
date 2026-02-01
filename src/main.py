import time
import random
import threading
from src.gui import HIDConfigurator
from src.capture import ScreenScanner
from src.solver import CaptchaEngine
from src.config import load_config, save_config
from src.engine import InputEngine

class AppController:
    def __init__(self):
        self.config_data = load_config()
        self.scanner = ScreenScanner()
        self.input_engine = InputEngine()
        self.solver = None 
        self.is_running = False
        self.gui = HIDConfigurator(self)
        
        threading.Thread(target=self.initialize_engine, daemon=True).start()

    def initialize_engine(self):
        try:
            self.gui.after(0, lambda: self.gui.status_label.configure(text="● LOADING OCR ENGINE..."))
            
            # Load the actual engine logic
            self.solver = CaptchaEngine()
            
            self.gui.after(0, lambda: self.gui.status_label.configure(text="● SYSTEM READY", text_color="#2ecc71"))
            self.gui.log("✅ Engine Loaded & Logic Synced.")
            
        except Exception as e:
            self.gui.after(0, lambda: self.gui.status_label.configure(text="● LOAD FAILED", text_color="#e74c3c"))
            self.gui.log(f"❌ Engine Error: {e}")

    def _get_random_wait(self, range_str, default_min=0.5, default_max=0.7):
        try:
            if "-" in range_str:
                parts = range_str.split('-')
                low = float(parts[0].strip())
                high = float(parts[1].strip())
                return random.uniform(low, high)
            return float(range_str)
        except Exception:
            return random.uniform(default_min, default_max)

    def toggle_automation(self, settings):
        if not self.is_running:
            self.is_running = True
            
            self.config_data.update(settings)
            save_config(self.config_data)
            
            self.gui.log("🚀 SERVICE STARTED")
            self.automation_thread = threading.Thread(target=self.core_loop, daemon=True)
            self.automation_thread.start()
        else:
            self.is_running = False
            self.gui.log("🛑 SERVICE STOPPED")
            
        return self.is_running

    def core_loop(self):
        TARGET_X, TARGET_Y = 835, 680
        TARGET_COLOR = "#CC9B12"
        loop_count = 0 

        while self.is_running:
            try:
                # 1. Check for Captcha
                if self.scanner.check_pixel_color(TARGET_X, TARGET_Y, TARGET_COLOR, tolerance=25):
                    self.gui.log("🎯 CAPTCHA DETECTED")
                    cap = self.config_data.get("capture_settings", {"x": 815, "y": 530, "w": 288, "h": 70})
                    frame = self.scanner.capture_region(cap['x'], cap['y'], cap['w'], cap['h'])
                    captcha_text = self.solver.solve(frame)
                    
                    if captcha_text:
                        self.handle_captcha_sequence(captcha_text)
                        time.sleep(5)
                    continue

                # 2. Targeting Phase
                self.gui.log("🔍 Targeting...")
                self.input_engine.simulate_press('tab', 0.1, 0.2)
                
                # Apply the range-based wait from the GUI input
                wait_time = self._get_random_wait(self.config_data.get("tab_wait", "0.7-1.0"))
                time.sleep(wait_time)

                # 3. Primary Action
                primary_key = self.config_data.get("key", "f3")
                min_d = float(self.config_data.get("min_delay", 8.1))
                max_d = float(self.config_data.get("max_delay", 8.7))
                
                delay_ms = self.input_engine.simulate_press(primary_key, min_d, max_d)
                self.gui.log(f"⚔️ {primary_key.upper()} | {delay_ms}ms")
                
                # 4. Secondary Action (Conditional)
                if self.config_data.get("use_secondary", False):
                    loop_count += 1
                    target_freq = int(self.config_data.get("freq", 4))
                    
                    if loop_count >= target_freq:
                        sec_key = self.config_data.get("key2", "f4")
                        self.gui.log(f"🌟 SECONDARY TRIGGER: {sec_key.upper()}")

                        time.sleep(random.uniform(0.5, 1.2))
                        self.input_engine.simulate_press(sec_key, 0.1, 0.3)
                        loop_count = 0

            except Exception as e:
                self.gui.log(f"⚠️ Loop Error: {e}")
                time.sleep(1)

    def handle_captcha_sequence(self, text):
        try:
            time.sleep(random.uniform(1.5, 3.5))
            self.gui.log(f"⌨️ TYPING CAPTCHA: {text}")
            
            for char in text.lower():
                self.input_engine.simulate_press(char, 0.05, 0.15)
                time.sleep(random.uniform(0.05, 0.1))
                
            time.sleep(random.uniform(0.5, 1.0))
            self.input_engine.simulate_press('enter', 0.1, 0.2)
            self.gui.log("✅ CAPTCHA SUBMITTED")
            
        except Exception as e:
            self.gui.log(f"❌ Input Error: {e}")

    def run(self):
        self.gui.mainloop()

if __name__ == "__main__":
    app = AppController()
    app.run()