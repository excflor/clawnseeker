import time
import random
import threading
from src.gui import HIDConfigurator
from src.capture import ScreenScanner
from src.solver import CaptchaEngine
from src.config import load_config

class AppController:
    def __init__(self):
        self.config_data = load_config()
        self.scanner = ScreenScanner()
        
        # We don't load the solver here anymore to avoid freezing the window
        self.solver = None 
        
        self.gui = HIDConfigurator(self)
        
        # Start the engine loading in the background
        threading.Thread(target=self.initialize_engine, daemon=True).start()

    def initialize_engine(self):
        """Loads the OCR models without locking the GUI."""
        try:
            self.gui.progress_bar.set(0.2)
            self.gui.status_label.configure(text="Status: Loading OCR Models...")
            
            from src.solver import CaptchaEngine
            self.solver = CaptchaEngine()
            
            self.gui.progress_bar.set(1.0)
            self.gui.status_label.configure(text="Status: System Ready", text_color="green")
            self.gui.log("✅ Captcha Engine Loaded Successfully.")
            
            # Turn off the progress bar after a delay
            time.sleep(2)
            self.gui.progress_bar.pack_forget() 
            
        except Exception as e:
            self.gui.status_label.configure(text="Status: Load Failed", text_color="red")
            self.gui.log(f"❌ Engine Error: {e}")

    def toggle_automation(self):
        """Called by the Start/Stop button in GUI."""
        if not self.is_running:
            self.is_running = True
            self.gui.log("🚀 Automation Started")
            self.automation_thread = threading.Thread(target=self.core_loop, daemon=True)
            self.automation_thread.start()
        else:
            self.is_running = False
            self.gui.log("🛑 Automation Stopped")

    def core_loop(self):
        """The 'Brain' of ClawnSeeker."""
        while self.is_running:
            try:
                # 1. Get current capture settings from config/GUI
                cap = self.config_data.get("capture_settings", {"x": 815, "y": 530, "w": 288, "h": 70})
                
                # 2. Capture the designated area
                frame = self.scanner.capture_region(cap['x'], cap['y'], cap['w'], cap['h'])
                
                # 3. Attempt to solve (OCR)
                captcha_text = self.solver.solve(frame)
                
                if captcha_text:
                    self.gui.log(f"🧩 Captcha Detected: {captcha_text}")
                    self.handle_captcha_sequence(captcha_text)
                
                # 4. Standard loop delay to prevent high CPU usage
                time.sleep(0.5) 
                
            except Exception as e:
                self.gui.log(f"⚠️ Loop Error: {e}")
                self.is_running = False

    def handle_captcha_sequence(self, text):
        """Stealthy input sequence."""
        # A. Simulate 'Reaction Time' (Human reading the screen)
        time.sleep(random.uniform(1.5, 3.5))
        
        self.gui.log(f"⌨️ Typing: {text}")
        
        for char in text:
            # B. Variable latency between keypresses
            # In your driver.py, you would use interception here:
            # self.driver.type_key(char) 
            time.sleep(random.uniform(0.08, 0.18))
            
        # C. Press Enter to submit
        time.sleep(random.uniform(0.4, 0.8))
        self.gui.log("✅ Captcha Submitted")

    def run(self):
        self.gui.mainloop()

if __name__ == "__main__":
    app = AppController()
    app.run()