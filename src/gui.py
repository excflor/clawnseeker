import customtkinter as ctk
import ctypes
from ctypes import windll, Structure, c_long, byref
from datetime import datetime
import time
from src.config import load_config, save_config
from src.capture import ScreenScanner

class HIDConfigurator(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.scanner = ScreenScanner()
        self.config_data = load_config()

        # --- Tactical Carbon Theme ---
        self.bg_color = "#080808"     
        self.card_bg = "#121212"      
        self.accent = "#3b82f6"       
        self.border_color = "#1f1f1f" 
        self.text_dim = "#888888"
        self.radius = 4               

        self.title("CLAWNSEEKER")
        self.geometry("1100x750")
        self.configure(fg_color=self.bg_color)
        
        self.setup_ui()
        self.initialize_data()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=0) # Sidebar
        self.grid_columnconfigure(1, weight=1) # Main Settings
        self.grid_columnconfigure(2, weight=1) # Logs
        self.grid_rowconfigure(0, weight=1)

        # 1. SIDEBAR
        self.sidebar = ctk.CTkFrame(self, fg_color=self.card_bg, width=220, corner_radius=0, border_width=1, border_color=self.border_color)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="CLAWNSEEKER", font=("Impact", 24), text_color=self.accent).pack(pady=20)
        
        prof_card = self.create_card(self.sidebar, "MAP PROFILE")
        self.map_dropdown = ctk.CTkComboBox(prof_card, values=list(self.config_data["maps"].keys()), 
                                            command=self.on_map_change, state="readonly", font=("Consolas", 12))
        self.map_dropdown.pack(pady=10, padx=10, fill="x")
        
        btn_f = ctk.CTkFrame(prof_card, fg_color="transparent")
        btn_f.pack(fill="x", padx=10, pady=(0, 10))
        ctk.CTkButton(btn_f, text="NEW", fg_color="#1e293b", hover_color="#334155", font=("Consolas", 11), command=self.add_new_map).pack(side="left", expand=True, padx=2)
        ctk.CTkButton(btn_f, text="DEL", fg_color="#450a0a", hover_color="#7f1d1d", font=("Consolas", 11), command=self.delete_map).pack(side="left", expand=True, padx=2)

        self.btn_toggle = ctk.CTkButton(self.sidebar, text="INITIALIZE SERVICE", fg_color=self.accent, 
                                        height=50, font=("Consolas", 13, "bold"), corner_radius=self.radius,
                                        command=self.on_toggle)
        self.btn_toggle.pack(side="bottom", pady=20, padx=15, fill="x")

        # 2. CENTER PANEL
        self.center_panel = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.center_panel.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)

        # Targeting Section (Standardized Box Size)
        target_card = self.create_card(self.center_panel, "TARGETING SEQUENCE (TAB)")
        tf = ctk.CTkFrame(target_card, fg_color="transparent")
        tf.pack(fill="x", padx=15, pady=15)
        ctk.CTkLabel(tf, text="PRE-ACTION WAIT:", font=("Consolas", 11)).pack(side="left")
        self.entry_tab_wait = ctk.CTkEntry(tf, width=100, justify="center", fg_color="#0a0a0a", border_color=self.border_color)
        self.entry_tab_wait.pack(side="right") # Matches Key input width

        # Primary Action (Left Aligned)
        prime_card = self.create_card(self.center_panel, "PRIMARY ACTION")
        pf1 = ctk.CTkFrame(prime_card, fg_color="transparent")
        pf1.pack(fill="x", padx=15, pady=(15, 5))
        ctk.CTkLabel(pf1, text="PRIMARY KEY:", font=("Consolas", 11)).pack(side="left")
        self.entry_key = ctk.CTkEntry(pf1, width=100, justify="center", fg_color="#0a0a0a", border_color=self.border_color)
        self.entry_key.pack(side="right")
        
        pf2 = ctk.CTkFrame(prime_card, fg_color="transparent")
        pf2.pack(fill="x", padx=10, pady=5)
        self.entry_min = self.create_labeled_entry(pf2, "MIN (s)", 0)
        self.entry_max = self.create_labeled_entry(pf2, "MAX (s)", 1)

        ctk.CTkButton(prime_card, text="COMMIT TO PROFILE", font=("Consolas", 11), fg_color="transparent", 
                      border_width=1, border_color=self.border_color, hover_color="#1a1a1a", 
                      command=self.save_current_map).pack(pady=10, padx=15, fill="x")

        # Secondary Sequence (Left Aligned)
        sec_card = self.create_card(self.center_panel, "SECONDARY SEQUENCE")
        sf_top = ctk.CTkFrame(sec_card, fg_color="transparent")
        sf_top.pack(fill="x", padx=15, pady=5)
        self.check_secondary = ctk.CTkCheckBox(sf_top, text="ENABLE SECONDARY", font=("Consolas", 11), 
                                               border_color=self.accent, command=self.toggle_secondary_ui)
        self.check_secondary.pack(side="left", pady=10)

        sf_btm = ctk.CTkFrame(sec_card, fg_color="transparent")
        sf_btm.pack(fill="x", padx=10, pady=(0, 10))
        self.entry_key2 = self.create_labeled_entry(sf_btm, "KEY", 0, width=90)
        self.entry_freq = self.create_labeled_entry(sf_btm, "LOOPS", 1, width=90)

        # Capture & Interaction Zone
        cap_card = self.create_card(self.center_panel, "VISUAL & INTERACTION")
        
        # Capture Config
        cf = ctk.CTkFrame(cap_card, fg_color="transparent")
        cf.pack(fill="x", padx=10, pady=(10, 5))
        ctk.CTkLabel(cf, text="CAPTURE ZONE:", font=("Consolas", 10, "bold"), text_color=self.text_dim).pack(anchor="w", padx=5)
        
        cf_in = ctk.CTkFrame(cf, fg_color="transparent")
        cf_in.pack(fill="x")
        self.entry_x = self.create_labeled_entry(cf_in, "X", 0, width=50)
        self.entry_y = self.create_labeled_entry(cf_in, "Y", 1, width=50)
        self.entry_w = self.create_labeled_entry(cf_in, "W", 2, width=50)
        self.entry_h = self.create_labeled_entry(cf_in, "H", 3, width=50)

        # Click Config (Before)
        cl_f = ctk.CTkFrame(cap_card, fg_color="transparent")
        cl_f.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(cl_f, text="CLICK (BEFORE):", font=("Consolas", 10, "bold"), text_color=self.text_dim).pack(anchor="w", padx=5)
        
        cl_in = ctk.CTkFrame(cl_f, fg_color="transparent")
        cl_in.pack(fill="x")
        self.check_click = ctk.CTkCheckBox(cl_in, text="ENABLE", font=("Consolas", 10), width=60)
        self.check_click.grid(row=0, column=0, padx=5, sticky="w")
        
        self.entry_cx = self.create_labeled_entry(cl_in, "CX", 1, width=50)
        self.entry_cy = self.create_labeled_entry(cl_in, "CY", 2, width=50)

        # Click Config (After)
        cl_f2 = ctk.CTkFrame(cap_card, fg_color="transparent")
        cl_f2.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(cl_f2, text="CLICK (AFTER):", font=("Consolas", 10, "bold"), text_color=self.text_dim).pack(anchor="w", padx=5)
        
        cl_in2 = ctk.CTkFrame(cl_f2, fg_color="transparent")
        cl_in2.pack(fill="x")
        self.check_click2 = ctk.CTkCheckBox(cl_in2, text="ENABLE", font=("Consolas", 10), width=60)
        self.check_click2.grid(row=0, column=0, padx=5, sticky="w")
        
        self.entry_cx2 = self.create_labeled_entry(cl_in2, "CX", 1, width=50)
        self.entry_cy2 = self.create_labeled_entry(cl_in2, "CY", 2, width=50)

        # Tools
        tf = ctk.CTkFrame(cap_card, fg_color="transparent")
        tf.pack(fill="x", padx=10, pady=10)
        
        # Row 1 Tools
        r1 = ctk.CTkFrame(tf, fg_color="transparent")
        r1.pack(fill="x", pady=2)
        self.btn_get_pos = ctk.CTkButton(r1, text="GET POS 1 (3s)", width=80, height=24, font=("Consolas", 9), 
                                         fg_color="#1a1a1a", border_width=1, border_color=self.border_color, 
                                         command=lambda: self.start_get_pos(1))
        self.btn_get_pos.pack(side="left", padx=2, expand=True)
        
        ctk.CTkButton(r1, text="TEST CLICK 1", width=80, height=24, font=("Consolas", 9), 
                      fg_color="#1a1a1a", border_width=1, border_color=self.border_color, 
                      command=lambda: self.test_click_action(1)).pack(side="left", padx=2, expand=True)

        # Row 2 Tools
        r2 = ctk.CTkFrame(tf, fg_color="transparent")
        r2.pack(fill="x", pady=2)
        self.btn_get_pos2 = ctk.CTkButton(r2, text="GET POS 2 (3s)", width=80, height=24, font=("Consolas", 9), 
                                         fg_color="#1a1a1a", border_width=1, border_color=self.border_color, 
                                         command=lambda: self.start_get_pos(2))
        self.btn_get_pos2.pack(side="left", padx=2, expand=True)
        
        ctk.CTkButton(r2, text="TEST CLICK 2", width=80, height=24, font=("Consolas", 9), 
                      fg_color="#1a1a1a", border_width=1, border_color=self.border_color, 
                      command=lambda: self.test_click_action(2)).pack(side="left", padx=2, expand=True)

        # 3. RIGHT PANEL (Logs)
        self.right_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.right_panel.grid(row=0, column=2, sticky="nsew", padx=(0, 15), pady=15)
        ctk.CTkLabel(self.right_panel, text="SYSTEM ACTIVITY STREAM", font=("Consolas", 11, "bold"), text_color=self.accent).pack(anchor="w")
        self.log_window = ctk.CTkTextbox(self.right_panel, font=("Consolas", 12), fg_color="#050505", 
                                         text_color="#00ff41", border_width=1, border_color=self.border_color)
        self.log_window.pack(fill="both", expand=True, pady=(5, 0))
        self.log_window.configure(state="disabled")

        # Footer
        self.footer = ctk.CTkFrame(self, fg_color=self.card_bg, height=30, corner_radius=0, border_width=1, border_color=self.border_color)
        self.footer.grid(row=1, column=0, columnspan=3, sticky="ew")
        
        self.status_label = ctk.CTkLabel(self.footer, text="● SYSTEM READY", font=("Consolas", 10), text_color="#2ecc71")
        self.status_label.pack(side="left", padx=20)

    # --- Utility Methods ---
    def create_card(self, parent, title):
        frame = ctk.CTkFrame(parent, fg_color=self.card_bg, corner_radius=self.radius, border_width=1, border_color=self.border_color)
        frame.pack(fill="x", pady=5, padx=5)
        header = ctk.CTkFrame(frame, fg_color=self.border_color, height=24, corner_radius=self.radius)
        header.pack(fill="x", side="top")
        ctk.CTkLabel(header, text=title.upper(), font=("Consolas", 10, "bold"), text_color=self.accent).pack(padx=10)
        return frame

    def create_labeled_entry(self, parent, label, col, width=90):
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.grid(row=0, column=col, padx=5, pady=5, sticky="w")
        ctk.CTkLabel(container, text=label, font=("Consolas", 9), text_color=self.text_dim).pack(anchor="w")
        entry = ctk.CTkEntry(container, width=width, justify="center", fg_color="#0a0a0a", border_color=self.border_color)
        entry.pack(anchor="w")
        return entry

    # --- Logic ---
    def initialize_data(self):
        last_map = self.config_data.get("last_selected_map", "default")
        self.map_dropdown.set(last_map)
        self.load_map_values(last_map)
        self.load_capture_values()
        self.toggle_secondary_ui()
        self.entry_tab_wait.insert(0, self.config_data.get("tab_wait", "0.7-1.0"))

    def load_map_values(self, name):
        data = self.config_data["maps"].get(name, {})
        self.entry_key.delete(0, "end")
        self.entry_key.insert(0, data.get("key", "3"))
        self.entry_min.delete(0, "end")
        self.entry_min.insert(0, str(data.get("min_delay", 9.4)))
        self.entry_max.delete(0, "end")
        self.entry_max.insert(0, str(data.get("max_delay", 9.6)))

    def load_capture_values(self):
        cap = self.config_data.get("capture_settings", {"x": 815, "y": 530, "w": 288, "h": 70})
        for entry, val in zip([self.entry_x, self.entry_y, self.entry_w, self.entry_h], [cap['x'], cap['y'], cap['w'], cap['h']]):
            entry.delete(0, "end")
            entry.insert(0, str(val))
            
        click = self.config_data.get("click_settings", {"enabled": False, "x": 0, "y": 0})
        self.check_click.select() if click.get("enabled") else self.check_click.deselect()
        self.entry_cx.delete(0, "end")
        self.entry_cx.insert(0, str(click.get("x", 0)))
        self.entry_cy.delete(0, "end")
        self.entry_cy.insert(0, str(click.get("y", 0)))

        click2 = self.config_data.get("click_settings_2", {"enabled": False, "x": 0, "y": 0})
        self.check_click2.select() if click2.get("enabled") else self.check_click2.deselect()
        self.entry_cx2.delete(0, "end")
        self.entry_cx2.insert(0, str(click2.get("x", 0)))
        self.entry_cy2.delete(0, "end")
        self.entry_cy2.insert(0, str(click2.get("y", 0)))

    def on_map_change(self, name):
        self.load_map_values(name)
        self.config_data["last_selected_map"] = name
        save_config(self.config_data)

    def save_current_map(self):
        name = self.map_dropdown.get()
        try:
            self.config_data["maps"][name] = {
                "key": self.entry_key.get().strip().lower(),
                "min_delay": float(self.entry_min.get()),
                "max_delay": float(self.entry_max.get())
            }
            save_config(self.config_data)
            self.log(f"PROFILE UPDATED: {name}")
        except: self.log("ERROR: INVALID INPUT")

    def toggle_secondary_ui(self):
        state = "normal" if self.check_secondary.get() == 1 else "disabled"
        self.entry_key2.configure(state=state)
        self.entry_freq.configure(state=state)

    def add_new_map(self):
        dialog = ctk.CTkInputDialog(text="Map Name:", title="New Profile")
        name = dialog.get_input()
        if name:
            self.config_data["maps"][name] = {"key": "3", "min_delay": 9.4, "max_delay": 9.6}
            save_config(self.config_data)
            self.map_dropdown.configure(values=list(self.config_data["maps"].keys()))
            self.map_dropdown.set(name)

    def delete_map(self):
        curr = self.map_dropdown.get()
        if len(self.config_data["maps"]) > 1:
            del self.config_data["maps"][curr]
            save_config(self.config_data)
            new_list = list(self.config_data["maps"].keys())
            self.map_dropdown.configure(values=new_list)
            self.map_dropdown.set(new_list[0])
            self.load_map_values(new_list[0])



    def start_get_pos(self, target_id):
        btn = self.btn_get_pos if target_id == 1 else self.btn_get_pos2
        btn.configure(text="MOVE NOW...", fg_color="#e74c3c")
        self.after(3000, lambda: self.finish_get_pos(target_id))

    class POINT(Structure):
        _fields_ = [("x", c_long), ("y", c_long)]

    def finish_get_pos(self, target_id):
        try:
            pt = self.POINT()
            windll.user32.GetCursorPos(byref(pt))
            x, y = pt.x, pt.y
            
            ex = self.entry_cx if target_id == 1 else self.entry_cx2
            ey = self.entry_cy if target_id == 1 else self.entry_cy2
            
            ex.delete(0, "end")
            ex.insert(0, str(x))
            ey.delete(0, "end")
            ey.insert(0, str(y))
            self.log(f"POS {target_id} CAPTURED: {x}, {y}")
        except Exception as e:
            self.log(f"POS ERROR: {e}")
        finally:
            btn = self.btn_get_pos if target_id == 1 else self.btn_get_pos2
            btn.configure(text=f"GET POS {target_id} (3s)", fg_color="#1a1a1a")

    def test_click_action(self, target_id):
        try:
            ex = self.entry_cx if target_id == 1 else self.entry_cx2
            ey = self.entry_cy if target_id == 1 else self.entry_cy2
            x = int(ex.get())
            y = int(ey.get())
            self.log(f"TESTING CLICK {target_id}: {x}, {y}")
            self.controller.input_engine.move_to(x, y)
            time.sleep(0.2)
            self.controller.input_engine.click()
        except Exception as e:
            self.log(f"CLICK ERROR: {e}")

    def log(self, msg):
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_window.configure(state="normal")
        self.log_window.insert("end", f"[{ts}] {msg}\n")
        self.log_window.see("end")
        self.log_window.configure(state="disabled")

    def on_toggle(self):
        settings = {
            "key": self.entry_key.get(),
            "min_delay": float(self.entry_min.get()),
            "max_delay": float(self.entry_max.get()),
            "use_secondary": bool(self.check_secondary.get()),
            "key2": self.entry_key2.get(),
            "freq": int(self.entry_freq.get() or 0),
            "tab_wait": self.entry_tab_wait.get(),
            "capture_settings": {
                "x": int(self.entry_x.get()), "y": int(self.entry_y.get()),
                "w": int(self.entry_w.get()), "h": int(self.entry_h.get())
            },
            "click_settings": {
                "enabled": bool(self.check_click.get()),
                "x": int(self.entry_cx.get()), "y": int(self.entry_cy.get())
            },
            "click_settings_2": {
                "enabled": bool(self.check_click2.get()),
                "x": int(self.entry_cx2.get()), "y": int(self.entry_cy2.get())
            }
        }
        active = self.controller.toggle_automation(settings)
        self.btn_toggle.configure(text="STOP SERVICE" if active else "INITIALIZE SERVICE", fg_color="#7f1d1d" if active else self.accent)
        self.status_label.configure(text="● ACTIVE" if active else "● READY", text_color="#e74c3c" if active else "#2ecc71")