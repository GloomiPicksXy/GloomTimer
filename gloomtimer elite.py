import customtkinter as ctk
import keyboard
import time
import json
import os
import threading
import random
from datetime import datetime
from PIL import Image, ImageTk  # Optional: for icons if you add images


class AutoTimeApp:
    def __init__(self, master):
        self.master = master
        self.master.title("AutoTime • Elite Edition")
        self.master.resizable(True, True)
        
        # Core variables
        self.q_delay = 0.0
        self.r_delay = 0.0
        self.is_enabled = True
        self.random_variance = 0  # ms
        self.current_config = None
        
        # Appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Window centering
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        window_width = 520
        window_height = 620
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Main container
        self.main_frame = ctk.CTkFrame(master=self.master, fg_color="#1a1a1a")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        self.header = ctk.CTkFrame(self.main_frame, height=80, fg_color="#111111")
        self.header.pack(fill="x", pady=(0, 15))
        self.header.pack_propagate(False)
        
        self.title_label = ctk.CTkLabel(
            self.header, 
            text="AUTOTIME",
            font=ctk.CTkFont(family="Roboto", size=32, weight="bold"),
            text_color="#00ffcc"
        )
        self.title_label.pack(side="left", padx=20, pady=15)
        
        self.version_label = ctk.CTkLabel(
            self.header, 
            text="v2.1 • PRO",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.version_label.pack(side="right", padx=20)
        
        # Status bar
        self.status_frame = ctk.CTkFrame(self.main_frame, height=30, fg_color="#222222")
        self.status_frame.pack(fill="x", pady=(0, 10))
        self.status_frame.pack_propagate(False)
        
        self.status_label = ctk.CTkLabel(
            self.status_frame, 
            text="Ready • Listening for Q & R",
            font=ctk.CTkFont(size=13),
            text_color="#00ff88"
        )
        self.status_label.pack(pady=6)
        
        # Tabview
        self.tabview = ctk.CTkTabview(self.main_frame, fg_color="#1f1f1f")
        self.tabview.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.tabview.add("Controls")
        self.tabview.add("Configs")
        self.tabview.add("Advanced")
        self.tabview.add("About")
        
        # ==================== CONTROLS TAB ====================
        controls_tab = self.tabview.tab("Controls")
        
        # Delay settings with sliders + entries
        self.create_delay_section(controls_tab)
        
        # Quick actions
        quick_frame = ctk.CTkFrame(controls_tab)
        quick_frame.pack(pady=15, padx=20, fill="x")
        
        self.toggle_button = ctk.CTkButton(
            quick_frame, 
            text="DISABLE AUTO",
            fg_color="#ff4444",
            hover_color="#cc0000",
            command=self.toggle_enabled,
            width=140,
            height=40,
            font=ctk.CTkFont(weight="bold")
        )
        self.toggle_button.pack(side="left", padx=10)
        
        self.test_q_btn = ctk.CTkButton(
            quick_frame, 
            text="Test Q",
            command=lambda: self.simulate_press('q'),
            width=100,
            height=40
        )
        self.test_q_btn.pack(side="left", padx=5)
        
        self.test_r_btn = ctk.CTkButton(
            quick_frame, 
            text="Test R",
            command=lambda: self.simulate_press('r'),
            width=100,
            height=40
        )
        self.test_r_btn.pack(side="left", padx=5)
        
        # ==================== CONFIGS TAB ====================
        configs_tab = self.tabview.tab("Configs")
        self.create_config_section(configs_tab)
        
        # ==================== ADVANCED TAB ====================
        adv_tab = self.tabview.tab("Advanced")
        self.create_advanced_section(adv_tab)
        
        # ==================== ABOUT TAB ====================
        about_tab = self.tabview.tab("About")
        self.create_about_section(about_tab)
        
        # Keyboard bindings
        keyboard.on_press_key('q', self.on_q_pressed, suppress=False)
        keyboard.on_press_key('r', self.on_r_pressed, suppress=False)
        
        # Load last config if exists
        self.auto_load_last_config()
        
        # Keyboard listener thread (for visual feedback)
        self.listener_active = True

    def create_delay_section(self, parent):
        frame = ctk.CTkFrame(parent)
        frame.pack(pady=15, padx=20, fill="x")
        
        # Q Delay
        q_frame = ctk.CTkFrame(frame, fg_color="transparent")
        q_frame.pack(fill="x", pady=8)
        
        ctk.CTkLabel(q_frame, text="Shooting (Q) Delay", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w")
        
        self.q_slider = ctk.CTkSlider(q_frame, from_=0, to=500, number_of_steps=500, command=self.update_q_from_slider)
        self.q_slider.set(0)
        self.q_slider.pack(fill="x", pady=5)
        
        q_entry_frame = ctk.CTkFrame(q_frame, fg_color="transparent")
        q_entry_frame.pack(fill="x")
        
        self.entry_q = ctk.CTkEntry(q_entry_frame, width=80, placeholder_text="ms")
        self.entry_q.pack(side="left")
        self.entry_q.bind("<Return>", lambda e: self.set_q_delay())
        
        ctk.CTkButton(q_entry_frame, text="Set Q", width=80, command=self.set_q_delay).pack(side="right")
        
        # R Delay
        r_frame = ctk.CTkFrame(frame, fg_color="transparent")
        r_frame.pack(fill="x", pady=8)
        
        ctk.CTkLabel(r_frame, text="Layup (R) Delay", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w")
        
        self.r_slider = ctk.CTkSlider(r_frame, from_=0, to=500, number_of_steps=500, command=self.update_r_from_slider)
        self.r_slider.set(0)
        self.r_slider.pack(fill="x", pady=5)
        
        r_entry_frame = ctk.CTkFrame(r_frame, fg_color="transparent")
        r_entry_frame.pack(fill="x")
        
        self.entry_r = ctk.CTkEntry(r_entry_frame, width=80, placeholder_text="ms")
        self.entry_r.pack(side="left")
        self.entry_r.bind("<Return>", lambda e: self.set_r_delay())
        
        ctk.CTkButton(r_entry_frame, text="Set R", width=80, command=self.set_r_delay).pack(side="right")

    def create_config_section(self, parent):
        # Save new config
        save_frame = ctk.CTkFrame(parent)
        save_frame.pack(pady=10, padx=20, fill="x")
        
        self.config_name_entry = ctk.CTkEntry(save_frame, placeholder_text="Config Name (e.g. Aggressive)")
        self.config_name_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        
        ctk.CTkButton(
            save_frame, 
            text="💾 Save", 
            width=100,
            command=self.save_config
        ).pack(side="right")
        
        # Config list
        list_frame = ctk.CTkFrame(parent)
        list_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        ctk.CTkLabel(list_frame, text="Saved Configurations", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0,8))
        
        self.config_listbox = ctk.CTkScrollableFrame(list_frame, height=180)
        self.config_listbox.pack(fill="both", expand=True)
        
        self.refresh_config_list()
        
        # Bottom buttons
        btn_frame = ctk.CTkFrame(parent)
        btn_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(btn_frame, text="🔄 Refresh", command=self.refresh_config_list, width=100).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🗑 Delete Selected", command=self.delete_selected_config, fg_color="#ff4444", width=140).pack(side="right", padx=5)

    def create_advanced_section(self, parent):
        frame = ctk.CTkFrame(parent)
        frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Random variance
        ctk.CTkLabel(frame, text="Random Variance (± ms)", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", pady=(10,5))
        
        self.variance_slider = ctk.CTkSlider(frame, from_=0, to=80, number_of_steps=80, command=self.update_variance)
        self.variance_slider.set(0)
        self.variance_slider.pack(fill="x", pady=5)
        
        self.variance_label = ctk.CTkLabel(frame, text="0 ms")
        self.variance_label.pack()
        
        # Theme selector
        ctk.CTkLabel(frame, text="Theme", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", pady=(20,5))
        
        self.theme_menu = ctk.CTkOptionMenu(
            frame,
            values=["Dark", "Light", "System"],
            command=self.change_theme
        )
        self.theme_menu.pack(fill="x")
        
        # Extra toggles
        self.random_toggle = ctk.CTkCheckBox(frame, text="Enable Random Timing", command=self.toggle_random)
        self.random_toggle.pack(anchor="w", pady=15)
        
        ctk.CTkButton(
            frame, 
            text="Reset All Settings", 
            fg_color="#444444",
            command=self.reset_all
        ).pack(pady=20)

    def create_about_section(self, parent):
        text = """AutoTime Elite
A powerful macro timing assistant.

Features:
• Real-time key simulation
• Configurable delays with sliders
• Persistent JSON profiles
• Random variance for human-like play
• Dark aesthetic with smooth UI

Made for precision gameplay.
Use responsibly.
"""
        label = ctk.CTkLabel(
            parent, 
            text=text,
            font=ctk.CTkFont(size=14),
            justify="left",
            wraplength=400
        )
        label.pack(pady=30, padx=30)

    # ====================== HELPER METHODS ======================
    
    def update_q_from_slider(self, value):
        self.entry_q.delete(0, "end")
        self.entry_q.insert(0, str(int(value)))
    
    def update_r_from_slider(self, value):
        self.entry_r.delete(0, "end")
        self.entry_r.insert(0, str(int(value)))
    
    def update_variance(self, value):
        self.random_variance = int(value)
        self.variance_label.configure(text=f"{self.random_variance} ms")
    
    def set_q_delay(self):
        try:
            val = int(self.entry_q.get())
            self.q_delay = val / 1000.0
            self.q_slider.set(val)
            self.flash_status("Q delay updated ✓", "#00ff88")
        except ValueError:
            self.flash_status("Invalid Q delay!", "#ff4444")
    
    def set_r_delay(self):
        try:
            val = int(self.entry_r.get())
            self.r_delay = val / 1000.0
            self.r_slider.set(val)
            self.flash_status("R delay updated ✓", "#00ff88")
        except ValueError:
            self.flash_status("Invalid R delay!", "#ff4444")
    
    def toggle_enabled(self):
        self.is_enabled = not self.is_enabled
        if self.is_enabled:
            self.toggle_button.configure(text="DISABLE AUTO", fg_color="#ff4444")
            self.status_label.configure(text="Ready • Listening for Q & R", text_color="#00ff88")
        else:
            self.toggle_button.configure(text="ENABLE AUTO", fg_color="#00cc66")
            self.status_label.configure(text="PAUSED", text_color="#ffaa00")
    
    def flash_status(self, text, color="#00ff88"):
        self.status_label.configure(text=text, text_color=color)
        self.master.after(2500, lambda: self.status_label.configure(
            text="Ready • Listening for Q & R" if self.is_enabled else "PAUSED",
            text_color="#00ff88" if self.is_enabled else "#ffaa00"
        ))
    
    def get_actual_delay(self, base_delay):
        if self.random_variance > 0:
            variance_sec = random.randint(-self.random_variance, self.random_variance) / 1000.0
            return max(0.05, base_delay + variance_sec)
        return base_delay
    
    def on_q_pressed(self, event):
        if not self.is_enabled or self.q_delay <= 0:
            return
        delay = self.get_actual_delay(self.q_delay)
        threading.Thread(target=self.execute_press, args=(delay,), daemon=True).start()
    
    def on_r_pressed(self, event):
        if not self.is_enabled or self.r_delay <= 0:
            return
        delay = self.get_actual_delay(self.r_delay)
        threading.Thread(target=self.execute_press, args=(delay,), daemon=True).start()
    
    def execute_press(self, delay):
        try:
            keyboard.press('e')
            time.sleep(delay)
            keyboard.release('e')
        except:
            pass  # Keyboard might be blocked in some contexts
    
    def simulate_press(self, key):
        """For testing buttons"""
        if key == 'q':
            delay = self.get_actual_delay(self.q_delay)
        else:
            delay = self.get_actual_delay(self.r_delay)
        self.flash_status(f"Testing {key.upper()}...", "#ffff00")
        threading.Thread(target=self.execute_press, args=(delay,), daemon=True).start()
    
    # ====================== CONFIG MANAGEMENT ======================
    
    def save_config(self):
        name = self.config_name_entry.get().strip()
        if not name:
            self.flash_status("Enter a config name!", "#ff4444")
            return
        
        config = {
            "q_delay_ms": int(self.entry_q.get() or 0),
            "r_delay_ms": int(self.entry_r.get() or 0),
            "variance": self.random_variance,
            "saved_at": datetime.now().isoformat()
        }
        
        os.makedirs("cfg", exist_ok=True)
        path = os.path.join("cfg", f"{name}.json")
        
        try:
            with open(path, "w") as f:
                json.dump(config, f, indent=2)
            self.flash_status(f"Config '{name}' saved!", "#00ff88")
            self.refresh_config_list()
        except Exception as e:
            self.flash_status("Failed to save config", "#ff4444")
    
    def load_config(self, filename):
        path = os.path.join("cfg", filename)
        try:
            with open(path, "r") as f:
                config = json.load(f)
            
            self.entry_q.delete(0, "end")
            self.entry_q.insert(0, str(config.get("q_delay_ms", 0)))
            self.q_slider.set(config.get("q_delay_ms", 0))
            self.q_delay = config.get("q_delay_ms", 0) / 1000.0
            
            self.entry_r.delete(0, "end")
            self.entry_r.insert(0, str(config.get("r_delay_ms", 0)))
            self.r_slider.set(config.get("r_delay_ms", 0))
            self.r_delay = config.get("r_delay_ms", 0) / 1000.0
            
            self.random_variance = config.get("variance", 0)
            self.variance_slider.set(self.random_variance)
            self.variance_label.configure(text=f"{self.random_variance} ms")
            
            self.current_config = filename
            self.flash_status(f"Loaded: {filename}", "#00ffcc")
            
        except Exception as e:
            self.flash_status("Failed to load config", "#ff4444")
    
    def refresh_config_list(self):
        for widget in self.config_listbox.winfo_children():
            widget.destroy()
        
        configs = self.get_config_files()
        if not configs:
            ctk.CTkLabel(self.config_listbox, text="No saved configs yet.", text_color="gray").pack(pady=20)
            return
        
        for cfg in configs:
            btn = ctk.CTkButton(
                self.config_listbox,
                text=cfg.replace(".json", ""),
                anchor="w",
                height=35,
                command=lambda c=cfg: self.load_config(c)
            )
            btn.pack(fill="x", padx=5, pady=2)
    
    def delete_selected_config(self):
        # Simple implementation: user can delete via file manager, or enhance later
        self.flash_status("Use file explorer to delete or implement selection", "#ffff00")
    
    def get_config_files(self):
        if not os.path.exists("cfg"):
            return []
        return [f for f in os.listdir("cfg") if f.endswith(".json")]
    
    def auto_load_last_config(self):
        configs = self.get_config_files()
        if configs:
            # Load the most recently modified
            latest = max(configs, key=lambda f: os.path.getmtime(os.path.join("cfg", f)))
            self.load_config(latest)
    
    def toggle_random(self):
        pass  # Already handled via slider
    
    def change_theme(self, theme):
        if theme == "Light":
            ctk.set_appearance_mode("light")
        elif theme == "Dark":
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("system")
    
    def reset_all(self):
        if ctk.CTkToplevel.askyesno("Reset", "Reset all settings to default?"):
            self.q_delay = self.r_delay = 0
            self.random_variance = 0
            self.entry_q.delete(0, "end")
            self.entry_r.delete(0, "end")
            self.q_slider.set(0)
            self.r_slider.set(0)
            self.variance_slider.set(0)
            self.flash_status("All settings reset", "#ffff00")


def main():
    app = ctk.CTk()
    AutoTimeApp(app)
    app.mainloop()


if __name__ == "__main__":
    main()
