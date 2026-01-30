import threading
import time
from src.gui import HIDConfigurator
from src.engine import InputEngine

class AppController:
    def __init__(self):
        self.engine = InputEngine()
        self.running = False
        self.settings = {}
        self.thread = None
        self.gui = HIDConfigurator(self)

    def toggle_bot(self, settings):
        self.settings = settings
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run_bot, daemon=True)
            self.thread.start()
            return True
        else:
            self.running = False
            self.gui.log("Stopping service...")
            return False

    def _run_bot(self):
        count = 0
        self.gui.after(0, self.gui.log, "Service Active")
        
        while self.running:
            try:
                key = self.settings['key']
                
                # Primary press
                ms_wait = self.engine.simulate_press(
                    key, 
                    self.settings['min_delay'], 
                    self.settings['max_delay']
                )
                self.gui.after(0, self.gui.log, f"Pressed {key} ({ms_wait}ms)")

                if self.settings.get('use_secondary'):
                    count += 1
                    if count >= self.settings['freq']:
                        key2 = self.settings['key2']
                        sec_ms = self.engine.simulate_press(key2, 0.5, 1.2)
                        self.gui.after(0, self.gui.log, f"Cheer: {key2} ({sec_ms}ms)")
                        count = 0
                        
            except Exception as e:
                self.gui.after(0, self.gui.log, f"ERROR: {e}")
                time.sleep(2)

    def run(self):
        self.gui.mainloop()

if __name__ == "__main__":
    app = AppController()
    app.run()