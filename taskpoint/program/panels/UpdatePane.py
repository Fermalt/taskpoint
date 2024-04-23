import tkinter as tk

from tkinter import font
from taskpoint.data.strings import UpdatesStrings as us
from taskpoint.program.utils.GenericFunctions import scroll_binding


class UpdatePane:
    def __init__(self, master):
        self.main_frame = master.main_frame
        self.master = master

        self.create_widgets()

    def create_widgets(self):
        canvas = tk.Canvas(self.main_frame)

        scrollbar = tk.Scrollbar(canvas, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="both")

        buttons_frame = tk.Frame(canvas)
        buttons_frame.pack(fill="both", expand=True)
        buttons_frame.update_idletasks()
        canvas.create_window((0, 0), window=buttons_frame, width=buttons_frame.winfo_width())

        # Creating the updates boxes
        title_dict = {}
        description_dict = {}
        i = len(us.updateDict) - 1
        for _ in us.updateDict:
            update = tk.Frame(buttons_frame, padx=5, pady=5)
            update.grid(row=len(us.updateDict)-i, column=0, sticky="w", pady=10)
            title_name = "Title" + str(i)
            title_dict[title_name] = tk.Label(update, text=getattr(us, title_name),
                                              font=font.Font(size=14, weight="bold"))
            title_dict[title_name].grid(row=0, column=0, sticky="w")

            description_name = "Description" + str(i)
            description_dict[description_name] = tk.Label(update,
                                                          text=getattr(us, description_name), justify="left",
                                                          wraplength=(buttons_frame.winfo_width() - 21),
                                                          font=font.Font(size=12))
            description_dict[description_name].grid(row=1, column=0, sticky="w")
            i -= 1

        buttons_frame.update_idletasks()

        scroll_binding(canvas, scrollbar, buttons_frame)
