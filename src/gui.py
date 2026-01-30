import customtkinter as ctk
from datetime import datetime
from src.config import load_config, save_config
from src.capture import ScreenScanner

class HIDConfigurator(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.scanner = ScreenScanner()
        self.config_data = load_config()

        # Window Setup
        self.title("CLAWNSEEKER DASHBOARD")
        self.geometry("950x660")
        self.configure(fg_color="#121212")
        
        # UI Constants
        self.accent = "#1f6aa5"
        self.card_bg = "#1c1c1c"
        
        self.setup_ui()
        self.initialize_data()

    def setup_ui(self):
        """Main UI Layout assembly."""
        # Main split container
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(side="top", fill="both", expand=True, padx=20, pady=20)

        # Left Column (Settings)
        self.left_wing = ctk.CTkFrame(self.main_container, fg_color="transparent", width=400)
        self.left_wing.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Right Column (Logs)
        self.right_wing = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.right_wing.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # Build Components
        self.build_header()
        
        self.scroll_frame = ctk.CTkScrollableFrame(self.left_wing, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True)

        self.build_profile_section()
        self.build_hardware_section()
        self.build_cheer_section()
        self.build_capture_section()

        # Big Launch Button
        self.btn_toggle = ctk.CTkButton(self.left_wing, text="INITIALIZE SERVICE", fg_color=self.accent, 
                                        height=55, font=("Arial", 16, "bold"), command=self.on_toggle)
        self.btn_toggle.pack(pady=(15, 0), fill="x")

        self.build_log_section()
        self.build_footer()

    # --- Component Builders ---
    def build_header(self):
        ctk.CTkLabel(self.left_wing, text="CLAWNSEEKER", font=("Impact", 32), text_color=self.accent).pack(anchor="w", pady=(0, 10))

    def build_profile_section(self):
        card = self.create_card(self.scroll_frame, "MAP PROFILE")
        f = ctk.CTkFrame(card, fg_color="transparent")
        f.pack(pady=10, fill="x", padx=10)

        self.map_dropdown = ctk.CTkComboBox(f, values=list(self.config_data["maps"].keys()), 
                                            command=self.on_map_change, state="readonly")
        self.map_dropdown.pack(side="left", expand=True, fill="x", padx=(0, 5))
        
        ctk.CTkButton(f, text="＋", width=35, fg_color="#2ecc71", command=self.add_new_map).pack(side="left", padx=2)
        ctk.CTkButton(f, text="－", width=35, fg_color="#e74c3c", command=self.delete_map).pack(side="left", padx=2)

    def build_hardware_section(self):
        card = self.create_card(self.scroll_frame, "HARDWARE PARAMETERS")
        
        ctk.CTkLabel(card, text="PRIMARY KEY", font=("Arial", 10)).pack()
        self.entry_key = ctk.CTkEntry(card, placeholder_text="f3", justify="center")
        self.entry_key.pack(pady=5, padx=20, fill="x")
        
        f = ctk.CTkFrame(card, fg_color="transparent")
        f.pack(pady=5)
        self.entry_min = self.create_labeled_entry(f, "MIN (s)", 0)
        self.entry_max = self.create_labeled_entry(f, "MAX (s)", 1)

        ctk.CTkButton(card, text="COMMIT TO PROFILE", font=("Arial", 11, "bold"), fg_color="transparent", 
                      border_width=1, border_color=self.accent, command=self.save_current_map).pack(pady=10, padx=20, fill="x")

    def build_cheer_section(self):
        card = self.create_card(self.scroll_frame, "CHEER SEQUENCE")
        self.check_secondary = ctk.CTkCheckBox(card, text="ENABLE CHEER", command=self.toggle_secondary_ui)
        self.check_secondary.pack(pady=10)

        f = ctk.CTkFrame(card, fg_color="transparent")
        f.pack(pady=(0, 10))
        self.entry_key2 = self.create_labeled_entry(f, "KEY", 0, width=80)
        self.entry_freq = self.create_labeled_entry(f, "LOOPS", 1, width=80)

    def build_capture_section(self):
        card = self.create_card(self.scroll_frame, "VISUAL CAPTURE ZONE")
        f = ctk.CTkFrame(card, fg_color="transparent")
        f.pack(pady=5)
        
        self.entry_x = self.create_labeled_entry(f, "X", 0, width=60)
        self.entry_y = self.create_labeled_entry(f, "Y", 1, width=60)
        self.entry_w = self.create_labeled_entry(f, "W", 2, width=60)
        self.entry_h = self.create_labeled_entry(f, "H", 3, width=60)

        ctk.CTkButton(card, text="TEST CAPTURE", fg_color="transparent", border_width=1, 
                      border_color="#f39c12", command=self.test_screen_capture).pack(pady=10, padx=20, fill="x")

    def build_log_section(self):
        ctk.CTkLabel(self.right_wing, text="SYSTEM ACTIVITY STREAM", font=("Arial", 11, "bold"), text_color=self.accent).pack(anchor="w")
        self.log_window = ctk.CTkTextbox(self.right_wing, font=("Consolas", 12), fg_color="#000", text_color="#0f0", border_width=1, border_color="#333")
        self.log_window.pack(fill="both", expand=True, pady=(5, 0))
        self.log_window.configure(state="disabled")

    def build_footer(self):
        self.footer = ctk.CTkFrame(self, fg_color="#181818", height=35, corner_radius=0)
        self.footer.pack(side="bottom", fill="x")
        
        self.status_label = ctk.CTkLabel(self.footer, text="STATUS: READY", font=("Consolas", 11))
        self.status_label.pack(side="left", padx=20)
        
        self.progress_bar = ctk.CTkProgressBar(self.footer, width=200)
        self.progress_bar.pack(side="right", padx=20)
        self.progress_bar.set(0)

    # --- UI Helpers ---
    def create_card(self, parent, title):
        frame = ctk.CTkFrame(parent, fg_color=self.card_bg, corner_radius=12)
        frame.pack(fill="x", pady=8, padx=5)
        ctk.CTkLabel(frame, text=title, font=("Arial", 10, "bold"), text_color=self.accent).pack(pady=(10, 0))
        return frame

    def create_labeled_entry(self, parent, label, col, width=100):
        ctk.CTkLabel(parent, text=label, font=("Arial", 10, "bold"), text_color="#888").grid(row=0, column=col, padx=5)
        entry = ctk.CTkEntry(parent, width=width, justify="center")
        entry.grid(row=1, column=col, padx=5, pady=5)
        return entry

    # --- Logic Methods ---
    def initialize_data(self):
        last_map = self.config_data.get("last_selected_map", "default")
        self.map_dropdown.set(last_map)
        self.load_map_values(last_map)
        self.load_capture_values()
        self.toggle_secondary_ui()

    def add_new_map(self):
        dialog = ctk.CTkInputDialog(text="Enter New Map Name:", title="Profile Creation")
        name = dialog.get_input()
        if name and name.strip():
            name = name.strip()
            self.config_data["maps"][name] = {
                "key": self.entry_key.get(),
                "min_delay": float(self.entry_min.get() or 8.1),
                "max_delay": float(self.entry_max.get() or 8.7)
            }
            save_config(self.config_data)
            self.map_dropdown.configure(values=list(self.config_data["maps"].keys()))
            self.map_dropdown.set(name)
            self.log(f"NEW PROFILE CREATED: {name}")

    def delete_map(self):
        current_map = self.map_dropdown.get()
        if len(self.config_data["maps"]) > 1:
            del self.config_data["maps"][current_map]
            new_list = list(self.config_data["maps"].keys())
            self.map_dropdown.configure(values=new_list)
            self.map_dropdown.set(new_list[0])
            self.load_map_values(new_list[0])
            save_config(self.config_data)
            self.log(f"REMOVED PROFILE: {current_map}")
        else:
            self.log("ERROR: CANNOT DELETE LAST PROFILE")

    def load_capture_values(self):
        cap = self.config_data.get("capture_settings", {"x": 815, "y": 530, "w": 288, "h": 70})
        for entry, val in zip([self.entry_x, self.entry_y, self.entry_w, self.entry_h], [cap['x'], cap['y'], cap['w'], cap['h']]):
            entry.delete(0, "end")
            entry.insert(0, str(val))

    def test_screen_capture(self):
        try:
            x, y, w, h = [int(e.get()) for e in [self.entry_x, self.entry_y, self.entry_w, self.entry_h]]
            self.config_data["capture_settings"] = {"x": x, "y": y, "w": w, "h": h}
            save_config(self.config_data)
            
            img = self.scanner.capture_region(x, y, w, h)
            path = self.scanner.save_debug_image(img)
            self.log(f"DEBUG CAPTURE SAVED: {path}")
        except Exception as e:
            self.log(f"CAPTURE ERROR: {e}")

    def on_map_change(self, name):
        self.load_map_values(name)
        self.config_data["last_selected_map"] = name
        save_config(self.config_data)
        self.log(f"PROFILE SWAP: {name}")

    def load_map_values(self, name):
        data = self.config_data["maps"].get(name, {})
        self.entry_key.delete(0, "end")
        self.entry_key.insert(0, data.get("key", "f3"))
        self.entry_min.delete(0, "end")
        self.entry_min.insert(0, str(data.get("min_delay", 8.1)))
        self.entry_max.delete(0, "end")
        self.entry_max.insert(0, str(data.get("max_delay", 8.7)))

    def save_current_map(self):
        name = self.map_dropdown.get()
        try:
            self.config_data["maps"][name] = {
                "key": self.entry_key.get().strip().lower(),
                "min_delay": float(self.entry_min.get()),
                "max_delay": float(self.entry_max.get())
            }
            save_config(self.config_data)
            self.log(f"UPDATED PROFILE: {name}")
        except ValueError:
            self.log("ERROR: CHECK DELAY FORMAT")

    def toggle_secondary_ui(self):
        state = "normal" if self.check_secondary.get() == 1 else "disabled"
        self.entry_key2.configure(state=state)
        self.entry_freq.configure(state=state)

    def log(self, msg):
        time_str = datetime.now().strftime("%H:%M:%S")
        self.log_window.configure(state="normal")
        self.log_window.insert("end", f"> {time_str} | {msg}\n")
        self.log_window.see("end")
        self.log_window.configure(state="disabled")

    def on_toggle(self):
        try:
            settings = {
                "key": self.entry_key.get().strip().lower(),
                "min_delay": float(self.entry_min.get()),
                "max_delay": float(self.entry_max.get()),
                "use_secondary": bool(self.check_secondary.get()),
                "key2": self.entry_key2.get().strip().lower() or "f4",
                "freq": int(self.entry_freq.get() or 4)
            }
            active = self.controller.toggle_automation(settings)
            self.btn_toggle.configure(
                text="TERMINATE SERVICE" if active else "INITIALIZE SERVICE",
                fg_color="#943126" if active else self.accent
            )
        except ValueError:
            self.log("ERROR: INVALID PARAMETERS")