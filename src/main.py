import time
import random
import threading
from src.gui import HIDConfigurator
from src.capture import ScreenScanner
from src.solver import CaptchaEngine
from src.config import load_config
from src.engine import InputEngine

class AppController:
    def __init__(self):
        self.config_data = load_config()
        self.scanner = ScreenScanner()
        self.input_engine = InputEngine()
        self.solver = None 
        self.gui = HIDConfigurator(self)
        
        # Start the engine loading in the background
        threading.Thread(target=self.initialize_engine, daemon=True).start()

    def initialize_engine(self):
        """Loads the OCR models without locking the GUI."""
        try:
            self.gui.progress_bar.set(0.2)
            self.gui.after(0, lambda: self.gui.status_label.configure(text="Status: Loading OCR Models..."))
            
            from src.solver import CaptchaEngine
            self.solver = CaptchaEngine()
            
            self.gui.progress_bar.set(1.0)
            self.gui.after(0, lambda: self.gui.status_label.configure(text="Status: System Ready", text_color="green"))
            self.gui.log("✅ Engine Loaded Successfully.")
            
            # Turn off the progress bar after a delay
            time.sleep(2)
            self.gui.progress_bar.pack_forget() 
            
        except Exception as e:
            self.gui.status_label.configure(text="Status: Load Failed", text_color="red")
            self.gui.log(f"❌ Engine Error: {e}")

    def toggle_automation(self, settings):
        """Called by the Start/Stop button in GUI."""
        if not hasattr(self, 'is_running'):
            self.is_running = False

        if not self.is_running:
            self.is_running = True
            
            self.config_data.update(settings)
            
            self.gui.log("🚀 STARTING AUTOMATION ENGINE")
            self.gui.log(f"📡 WATCHING PIXEL: [836, 605] | COLOR: #F7DD20")
            
            self.automation_thread = threading.Thread(target=self.core_loop, daemon=True)
            self.automation_thread.start()
        else:
            self.is_running = False
            self.gui.log("🛑 AUTOMATION STOPPED")
            
        return self.is_running

    def core_loop(self):
        self.is_running = True
        
        # Pull settings from the dictionary passed by the GUI
        primary_key = self.config_data.get("key", "f3")
        min_d = self.config_data.get("min_delay", 8.1)
        max_d = self.config_data.get("max_delay", 8.7)
        
        target_x, target_y = 835, 680
        target_color = "#CC9B12"

        while self.is_running:
            try:
                # --- TASK 1: THE PIXEL WATCHER ---
                if self.scanner.check_pixel_color(target_x, target_y, target_color, tolerance=25):
                    self.gui.log("🎯 CAPTCHA DETECTED - Pausing Service...")
                    
                    # Capture and Solve
                    self.gui.log("1...")
                    cap = self.config_data.get("capture_settings", {"x": 815, "y": 530, "w": 288, "h": 70})
                    self.gui.log("2...")
                    frame = self.scanner.capture_region(cap['x'], cap['y'], cap['w'], cap['h'])
                    self.gui.log("3...")
                    captcha_text = self.solver.solve(frame)
                    self.gui.log("4...")
                    
                    if captcha_text:
                        self.gui.log("Typing now...")
                        self.handle_captcha_sequence(captcha_text)
                        time.sleep(5)
                    continue

                # --- TASK 2: THE PRIMARY ACTION ---
                delay_ms = self.input_engine.simulate_press(primary_key, min_d, max_d)
                
                self.gui.log(f"⚔️ Action: {primary_key} | Delay: {delay_ms}ms")

            except Exception as e:
                self.gui.log(f"⚠️ Input Error: {e}")
                time.sleep(1)

    def handle_captcha_sequence(self, text):
        """Stealthy input sequence using the Interception driver."""
        try:
            # A. Simulate 'Reaction Time'
            time.sleep(random.uniform(1.5, 3.5))
            self.gui.log(f"⌨️ Typing via Driver: {text}")
            
            # Ensure text is lowercase as most game drivers prefer char-by-char
            for char in text.lower():
                # We use a very short delay for typing speed
                # Note: simulate_press handles the key_down and key_up
                self.input_engine.simulate_press(char, 0.05, 0.15)
                
            # C. Press Enter to submit
            time.sleep(random.uniform(0.5, 1.0))
            self.input_engine.simulate_press('enter', 0.1, 0.2)
            self.gui.log("✅ Captcha Submitted")
            
        except Exception as e:
            self.gui.log(f"❌ Typing Error: {e}")

    def run(self):
        self.gui.mainloop()

if __name__ == "__main__":
    app = AppController()
    app.run()