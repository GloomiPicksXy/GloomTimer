import customtkinter
import keyboard
import time
import json
import os

class AutoTimeApp:
    def __init__(self, master):
        self.master = master
        self.q_delay = 0
        self.r_delay = 0
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        window_width = 400
        window_height = 350
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.main_frame = customtkinter.CTkFrame(master=self.master)
        self.main_frame.pack(fill="both", expand=True)

        self.label = customtkinter.CTkLabel(master=self.main_frame, text="AutoTime", font=("Roboto", 24))
        self.label.pack(pady=6, padx=10)

        self.config_frame = customtkinter.CTkFrame(master=self.main_frame)
        self.config_frame.pack(pady=12, padx=10)

        self.label_q = customtkinter.CTkLabel(master=self.config_frame, text="Shooting (ms)")
        self.label_q.grid(row=0, column=0)
        self.entry_q = customtkinter.CTkEntry(master=self.config_frame)
        self.entry_q.grid(row=0, column=1)
        self.button_q = customtkinter.CTkButton(master=self.config_frame, text="Submit Q", command=self.set_q_delay)
        self.button_q.grid(row=0, column=2, pady=5, padx=5)

        self.label_r = customtkinter.CTkLabel(master=self.config_frame, text="Layup (ms)")
        self.label_r.grid(row=1, column=0)
        self.entry_r = customtkinter.CTkEntry(master=self.config_frame)
        self.entry_r.grid(row=1, column=1)
        self.button_r = customtkinter.CTkButton(master=self.config_frame, text="Submit R", command=self.set_r_delay)
        self.button_r.grid(row=1, column=2, pady=5, padx=5)

        self.config_name_entry = customtkinter.CTkEntry(master=self.main_frame, placeholder_text="Config Name")
        self.config_name_entry.pack(pady=6, padx=10)

        self.save_button = customtkinter.CTkButton(master=self.main_frame, text="Save Config", command=self.save_config)
        self.save_button.pack(pady=6, padx=10)

        self.config_dropdown = customtkinter.CTkOptionMenu(master=self.main_frame, values=self.get_config_files(), command=self.load_config)
        self.config_dropdown.pack(pady=12, padx=10)

        self.status_label = customtkinter.CTkLabel(master=self.main_frame, text="")
        self.status_label.pack(pady=6, padx=10)

        self.load_status_label = customtkinter.CTkLabel(master=self.main_frame, text="")
        self.load_status_label.pack(pady=6, padx=10)


        keyboard.on_press_key('q', self.on_q_pressed)
        keyboard.on_press_key('r', self.on_r_pressed)

    def set_q_delay(self):
        try:
            self.q_delay = int(self.entry_q.get()) / 1000 
            self.status_label.configure(text="Q delay set", text_color="green")
        except ValueError:
            self.status_label.configure(text="Invalid delay for Q", text_color="red")

    def set_r_delay(self):
        try:
            self.r_delay = int(self.entry_r.get()) / 1000
            self.status_label.configure(text="R delay set", text_color="green")
        except ValueError:
            self.status_label.configure(text="Invalid delay for R", text_color="red")

    def on_q_pressed(self, event):
        keyboard.press('e')
        time.sleep(self.q_delay)
        keyboard.release('e')

    def on_r_pressed(self, event):
        keyboard.press('e')
        time.sleep(self.r_delay)
        keyboard.release('e')

    def save_config(self):
        config_name = self.config_name_entry.get().strip()
        if config_name:
            config = {
                "q_delay": int(self.entry_q.get()),
                "r_delay": int(self.entry_r.get())
            }
            config_dir = "cfg"
            if not os.path.exists(config_dir):
                os.makedirs(config_dir)
            config_path = os.path.join(config_dir, f"{config_name}.json")
            with open(config_path, "w") as file:
                json.dump(config, file)
            self.status_label.configure(text=f"Config saved as {config_name}.json", text_color="green")
            self.update_config_dropdown()
        else:
            self.status_label.configure(text="Please enter a config name.", text_color="red")

    def load_config(self, config_name):
        config_dir = "cfg"
        config_path = os.path.join(config_dir, config_name)
        if os.path.exists(config_path):
            with open(config_path, "r") as file:
                config = json.load(file)
                self.entry_q.delete(0, customtkinter.END)
                self.entry_q.insert(0, config["q_delay"])
                self.entry_r.delete(0, customtkinter.END)
                self.entry_r.insert(0, config["r_delay"])
                self.q_delay = config["q_delay"] / 1000
                self.r_delay = config["r_delay"] / 1000
            self.status_label.configure(text=f"Config {config_name} loaded", text_color="green")
            self.load_status_label.configure(text=f"Config {config_name} loaded successfully")
        else:
            self.status_label.configure(text=f"Config {config_name} not found", text_color="red")
            self.load_status_label.configure(text=f"Config {config_name} not found", text_color="red")

    def get_config_files(self):
        config_dir = "cfg"
        if not os.path.exists(config_dir):
            return []
        return [f for f in os.listdir(config_dir) if f.endswith(".json")]

    def update_config_dropdown(self):
        self.config_dropdown.destroy()
        self.config_dropdown = customtkinter.CTkOptionMenu(master=self.main_frame, values=self.get_config_files(), command=self.load_config)
        self.config_dropdown.pack(pady=12, padx=10)


def main():
    app = customtkinter.CTk()
    AutoTimeApp(app)
    app.mainloop()

if __name__ == "__main__":
    main()
