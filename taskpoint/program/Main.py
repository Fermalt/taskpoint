import tkinter as tk

from ctypes import windll
from utils import Database
from panels.TaskList import TaskList


class App(tk.Tk):

    def __init__(self):
        super().__init__()

        windll.shcore.SetProcessDpiAwareness(1)

        self.title("TaskPoint")
        self.iconbitmap("../data/images/TaskPointLogo.ico")
        self.configure(bg="white")

        self.geometry("500x500")
        self.minsize(500, 250)
        self.maxsize(500, 1000)

        x = (self.winfo_screenwidth() - 200) // 2
        y = (self.winfo_screenheight() - 500) // 2

        # Set the window's position and size
        self.geometry(f"{500}x{500}+{x}+{y}")

        # Create the database
        Database.create_database()

        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(fill="both", expand=True)
        TaskList(self)
        self.mainloop()


"""This program is launch first as it is the main"""
if __name__ == '__main__':
    app = App()
