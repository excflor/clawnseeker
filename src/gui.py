import customtkinter as ctk
from datetime import datetime
from src.config import load_config, save_config
from src.capture import ScreenScanner

class HIDConfigurator(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.scanner = ScreenScanner()
        self.controller = controller
        self.title("CLAWNSEEKER // DASHBOARD")
        self.geometry("950x650") # Slightly larger for better breathing room
        
        # Color Palette
        self.accent_color = "#1f6aa5" 
        self.bg_color = "#121212"      # Slightly darker for depth
        self.card_color = "#1c1c1c"    # Card elevation
        self.footer_color = "#181818"  # Subtle footer distinction
        self.text_dim = "#888888"      
        
        ctk.set_appearance_mode("dark")
        self.configure(fg_color=self.bg_color)
        self.config_data = load_config()

        # --- TOP LEVEL CONTAINERS ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(side="top", fill="both", expand=True)

        self.footer_bar = ctk.CTkFrame(self, fg_color=self.footer_color, height=40, corner_radius=0)
        self.footer_bar.pack(side="bottom", fill="x")

        # --- MAIN SPLIT (Inside main_container) ---
        self.left_wing = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.left_wing.pack(side="left", fill="both", expand=True, padx=(20, 10), pady=20)

        self.right_wing = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.right_wing.pack(side="right", fill="both", expand=True, padx=(10, 20), pady=20)

        # --- LEFT WING CONTENT (Settings) ---
        self.header_label = ctk.CTkLabel(self.left_wing, text="CLAWNSEEKER", font=("Impact", 28), text_color=self.accent_color)
        self.header_label.pack(pady=(0, 15), anchor="w")

        # Scrollable area for settings to keep it tidy
        self.settings_scroll = ctk.CTkScrollableFrame(self.left_wing, fg_color="transparent", width=380, height=350)
        self.settings_scroll.pack(fill="both", expand=True)

        # Profile Card
        self.profile_card = self.create_card(self.settings_scroll, "MAP PROFILE")
        map_mgmt_frame = ctk.CTkFrame(self.profile_card, fg_color="transparent")
        map_mgmt_frame.pack(pady=10, fill="x", padx=10)

        self.map_dropdown = ctk.CTkComboBox(
            map_mgmt_frame, values=list(self.config_data["maps"].keys()), 
            command=self.on_map_change, height=35, border_color="#444444",
            button_color=self.accent_color, fg_color="#121212", state="readonly"
        )
        self.map_dropdown.pack(side="left", padx=(0, 5), expand=True, fill="x")
        self.map_dropdown.set(self.config_data.get("last_selected_map", "default"))

        self.btn_add_map = ctk.CTkButton(map_mgmt_frame, text="＋", width=35, height=35, fg_color="#2ecc71", command=self.add_new_map)
        self.btn_add_map.pack(side="left", padx=2)
        
        self.btn_del_map = ctk.CTkButton(map_mgmt_frame, text="－", width=35, height=35, fg_color="#e74c3c", command=self.delete_map)
        self.btn_del_map.pack(side="left", padx=2)

        # Primary Settings Card
        self.primary_card = self.create_card(self.settings_scroll, "HARDWARE PARAMETERS")
        self.entry_key = ctk.CTkEntry(self.primary_card, placeholder_text="f3", border_color="#444444", justify="center", height=35)
        self.entry_key.pack(pady=10, padx=20, fill="x")

        delay_frame = ctk.CTkFrame(self.primary_card, fg_color="transparent")
        delay_frame.pack(pady=5)
        self.entry_min = self.create_labeled_entry(delay_frame, "MIN (s)", 0)
        self.entry_max = self.create_labeled_entry(delay_frame, "MAX (s)", 1)

        self.btn_save_map = ctk.CTkButton(self.primary_card, text="COMMIT TO PROFILE", font=("Arial", 11, "bold"),
                                          fg_color="transparent", border_width=1, border_color=self.accent_color,
                                          command=self.save_current_map_to_json)
        self.btn_save_map.pack(pady=10, padx=20, fill="x")

        # Cheer Card
        self.sec_card = self.create_card(self.settings_scroll, "CHEER SEQUENCE")
        self.check_secondary = ctk.CTkCheckBox(self.sec_card, text="ENABLE", command=self.toggle_secondary_ui, border_color=self.accent_color)
        self.check_secondary.pack(pady=10)

        sec_input_frame = ctk.CTkFrame(self.sec_card, fg_color="transparent")
        sec_input_frame.pack(pady=(0, 10))
        self.entry_key2 = ctk.CTkEntry(sec_input_frame, width=70, justify="center", placeholder_text="KEY")
        self.entry_freq = ctk.CTkEntry(sec_input_frame, width=70, justify="center", placeholder_text="LOOPS")
        self.entry_key2.grid(row=0, column=0, padx=5)
        self.entry_freq.grid(row=0, column=1, padx=5)

        self.capture_card = self.create_card(self.settings_scroll, "VISUAL CAPTURE ZONE")

        cap_grid = ctk.CTkFrame(self.capture_card, fg_color="transparent")
        cap_grid.pack(pady=10)

        # X and Y coordinates
        ctk.CTkLabel(cap_grid, text="X pos").grid(row=0, column=0)
        self.entry_x = ctk.CTkEntry(cap_grid, width=60, placeholder_text="0")
        self.entry_x.grid(row=1, column=0, padx=5)

        ctk.CTkLabel(cap_grid, text="Y pos").grid(row=0, column=1)
        self.entry_y = ctk.CTkEntry(cap_grid, width=60, placeholder_text="0")
        self.entry_y.grid(row=1, column=1, padx=5)

        # Width and Height
        ctk.CTkLabel(cap_grid, text="Width").grid(row=2, column=0, pady=(5,0))
        self.entry_w = ctk.CTkEntry(cap_grid, width=60, placeholder_text="100")
        self.entry_w.grid(row=3, column=0, padx=5)

        ctk.CTkLabel(cap_grid, text="Height").grid(row=2, column=1, pady=(5,0))
        self.entry_h = ctk.CTkEntry(cap_grid, width=60, placeholder_text="100")
        self.entry_h.grid(row=3, column=1, padx=5)

        # Test Button
        self.btn_test_cap = ctk.CTkButton(
            self.capture_card, 
            text="TEST CAPTURE & LOG", 
            fg_color="transparent", 
            border_width=1, 
            border_color="#f39c12",
            command=self.test_screen_capture
        )
        self.btn_test_cap.pack(pady=10, padx=20, fill="x")

        # Big Launch Button (Bottom of Left Wing)
        self.btn_toggle = ctk.CTkButton(self.left_wing, text="INITIALIZE SERVICE", fg_color=self.accent_color, 
                                        height=55, font=("Arial", 16, "bold"), command=self.on_toggle)
        self.btn_toggle.pack(pady=(15, 0), fill="x")

        # --- RIGHT WING CONTENT (The Big Log) ---
        ctk.CTkLabel(self.right_wing, text="SYSTEM ACTIVITY STREAM", font=("Arial", 11, "bold"), text_color=self.accent_color).pack(anchor="w", pady=(0, 10))
        
        self.log_window = ctk.CTkTextbox(
            self.right_wing, 
            font=("Consolas", 12), 
            fg_color="#000000", 
            text_color="#00ff00", 
            border_width=1, 
            border_color="#333333"
        )
        self.log_window.pack(fill="both", expand=True)
        self.log_window.configure(state="disabled")

        # --- FOOTER STATUS SECTION (Clean & Horizontal) ---
        # 1. Main Status Text
        self.status_label = ctk.CTkLabel(self.footer_bar, text="STATUS: READY", 
                                         font=("Consolas", 11), text_color=self.text_dim)
        self.status_label.pack(side="left", padx=(20, 10))

        self.progress_bar = ctk.CTkProgressBar(self.footer_bar, width=200, height=8, 
                                               progress_color=self.accent_color)
        self.progress_bar.pack(side="right", padx=20, pady=10)
        self.progress_bar.set(0)

        # Initial Load
        self.load_map_values(self.map_dropdown.get())
        self.load_capture_settings()
        self.toggle_secondary_ui()

    # --- UI HELPERS ---
    def create_card(self, parent, title):
        frame = ctk.CTkFrame(parent, fg_color=self.card_color, corner_radius=12)
        frame.pack(fill="x", pady=8, padx=5)
        ctk.CTkLabel(frame, text=title, font=("Arial", 10, "bold"), text_color=self.accent_color).pack(pady=(10, 0))
        return frame

    def create_labeled_entry(self, parent, label, col):
        ctk.CTkLabel(parent, text=label, font=("Arial", 10, "bold"), text_color=self.text_dim).grid(row=0, column=col)
        entry = ctk.CTkEntry(parent, width=100, border_color="#444444", justify="center")
        entry.grid(row=1, column=col, padx=10, pady=5)
        return entry

    # --- LOGIC METHODS ---
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
            self.log(f"NEW PROFILE: {name}")

    def delete_map(self):
        current_map = self.map_dropdown.get()
        if len(self.config_data["maps"]) > 1:
            del self.config_data["maps"][current_map]
            new_list = list(self.config_data["maps"].keys())
            self.map_dropdown.configure(values=new_list)
            self.map_dropdown.set(new_list[0])
            self.load_map_values(new_list[0])
            save_config(self.config_data)
            self.log(f"REMOVED: {current_map}")

    def load_capture_settings(self):
        # 1. Safely grab the settings (providing defaults if missing)
        cap = self.config_data.get("capture_settings", {"x": 815, "y": 530, "w": 288, "h": 70})
        
        # 2. Clear and Insert for each field
        self.entry_x.delete(0, "end")
        self.entry_x.insert(0, str(cap['x']))
        
        self.entry_y.delete(0, "end")
        self.entry_y.insert(0, str(cap['y']))
        
        self.entry_w.delete(0, "end")
        self.entry_w.insert(0, str(cap['w']))
        
        self.entry_h.delete(0, "end")
        self.entry_h.insert(0, str(cap['h']))

    def test_screen_capture(self):
        try:
            # 1. Get current values from GUI
            x, y = int(self.entry_x.get()), int(self.entry_y.get())
            w, h = int(self.entry_w.get()), int(self.entry_h.get())
            
            # 2. Update config_data and Save to JSON
            self.config_data["capture_settings"] = {"x": x, "y": y, "w": w, "h": h}
            save_config(self.config_data)
            
            # 3. Capture and Save Image
            img = self.scanner.capture_region(x, y, w, h)
            saved_path = self.scanner.save_debug_image(img)
            
            self.log(f"SAVED: Settings & {saved_path}")
        except Exception as e:
            self.log(f"CAPTURE ERROR: {e}")

    def on_map_change(self, map_name):
        self.load_map_values(map_name)
        self.log(f"MOUNTED: {map_name}")

    def load_map_values(self, map_name):
        map_data = self.config_data["maps"].get(map_name, {})
        self.entry_key.delete(0, "end")
        self.entry_key.insert(0, map_data.get("key", "f3"))
        self.entry_min.delete(0, "end")
        self.entry_min.insert(0, str(map_data.get("min_delay", 8.1)))
        self.entry_max.delete(0, "end")
        self.entry_max.insert(0, str(map_data.get("max_delay", 8.7)))

    def save_current_map_to_json(self):
        map_name = self.map_dropdown.get()
        try:
            self.config_data["maps"][map_name] = {
                "key": self.entry_key.get().strip().lower(),
                "min_delay": float(self.entry_min.get()),
                "max_delay": float(self.entry_max.get())
            }
            save_config(self.config_data)
            self.log(f"UPDATED: {map_name}")
        except ValueError:
            self.log("ERROR: INVALID DATA")

    def toggle_secondary_ui(self):
        state = "normal" if self.check_secondary.get() == 1 else "disabled"
        self.entry_key2.configure(state=state)
        self.entry_freq.configure(state=state)

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_window.configure(state="normal")
        self.log_window.insert("end", f"> {timestamp} | {message}\n")
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
            is_running = self.controller.toggle_automation(settings)
            self.btn_toggle.configure(
                text="TERMINATE SERVICE" if is_running else "INITIALIZE SERVICE",
                fg_color="#943126" if is_running else self.accent_color
            )
        except ValueError:
            self.log("ERROR: CHECK DELAY NUMBERS")