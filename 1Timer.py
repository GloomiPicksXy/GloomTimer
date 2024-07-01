# Hello There
import customtkinter
import keyboard
import time

class AutoTimeApp:
    def __init__(self, master):
        self.master = master
        self.q_delay = 0

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        window_width = 530
        window_height = 190
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.master.title("AutoTime By [GloomiPick]")

        self.main_frame = customtkinter.CTkFrame(master=self.master)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.label = customtkinter.CTkLabel(master=self.main_frame, text="AutoTime by [GloomiPicks]", font=("Roboto", 24))
        self.label.pack(pady=10)

        self.config_frame = customtkinter.CTkFrame(master=self.main_frame)
        self.config_frame.pack(pady=10, padx=10, fill="x")

        self.label_q = customtkinter.CTkLabel(master=self.config_frame, text="Shooting Delay (ms):", font=("Roboto", 14))
        self.label_q.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_q = customtkinter.CTkEntry(master=self.config_frame, font=("Roboto", 14))
        self.entry_q.grid(row=0, column=1, padx=10, pady=10)
        self.button_q = customtkinter.CTkButton(master=self.config_frame, text="Set Delay", command=self.set_q_delay)
        self.button_q.grid(row=0, column=2, padx=10, pady=10)

        self.status_label = customtkinter.CTkLabel(master=self.main_frame, text="", font=("Roboto", 12))
        self.status_label.pack(pady=10)

        keyboard.on_press_key('q', self.on_q_pressed) 

    def set_q_delay(self):
        try:
            self.q_delay = int(self.entry_q.get()) / 1000
            self.status_label.configure(text="Q delay set successfully", text_color="green")
        except ValueError:
            self.status_label.configure(text="Invalid delay value. Please enter a number.", text_color="red")

    def on_q_pressed(self, event):
        keyboard.press('e')
        time.sleep(self.q_delay)
        keyboard.release('e')

def main():
    app = customtkinter.CTk()
    AutoTimeApp(app)
    app.mainloop()

if __name__ == "__main__":
    main()
