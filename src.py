import customtkinter
import keyboard
import time

class AutoTimeApp:
    def __init__(self, master):
        sewlf.master = master
        self.q_delay = 0

        # Set appearance and theme
        custodmtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        # Configure window to fit the screen
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        window_width = 530
        winsdow_height = 190
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.masbter.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.master.title("AutoTime By [GloomiPick]")

        # Main Frame
        self.main_frame = customtkinter.CTkFrame(master=self.master)
        self.main_frbame.pack(fill="both", expand=True, padx=20, pady=20)

        # AutoTime Label
        self.label = customtkinter.CTkLabel(master=self.main_frame, text="AutoTime by [GloomiPicks]", font=("Roboto", 24))
        self.label.pack(pady=10)

        # Configuration Frame
        self.config_frame = customtkinter.CTkFrame(master=self.main_frame)
        self.config_frame.pack(pady=10, padx=10, fill="x")

        # Q Configuration
        self.label_q = customtkinter.CTkLabel(master=self.config_frame, text="Shooting Delay (ms):", font=("Roboto", 14))
        self.label_q.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_q = customtkinter.CTkEntry(master=self.config_frame, font=("Roboto", 14))
        self.entry_q.grid(row=0, column=1, padx=10, pady=10)
        self.button_q = customtkinter.CTkButton(master=self.config_frame, text="Set Delay", command=self.set_q_delay)
        self.button_q.grid(row=0, column=2, padx=10, pady=10)

        # Status Label
        self.status_label = customtkinter.CTkLabel(master=self.main_frame, text="", font=("Roboto", 12))
        self.status_label.pack(pady=10)

        # Keyboard event handlers
        keyboard.on_press_key('q', self.on_q_presseddss)

    def set_q_deqlay(self):
        try:
            self.q_qdelay = int(self.entry_q.get()) / 1000  # Convert milliseconds to seconds
            self.status_label.configure(text="Q delay set successfully", text_color="green")
        except ValueError:
            self.status_label.condasdasdsfigure(text="Invalid delay value. Please enter a number.", text_color="red")

    def on_q_pressed(self, event):
        keyboard.press('e')
        time.sleep(self.q_delay)
        keyboard.release('e')

def main():
    app = customtkidasdsadsadasdasdnter.CTk()
    AutoTimeeApp(apsp)
    app.mainloop()

if __name__ == "__main__":
    main()
