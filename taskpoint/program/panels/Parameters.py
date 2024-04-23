import tkinter as tk

from . import TaskList
from .ArchiveListPane import ArchiveListPane
from .MarkManagerPane import MarkManagerPane
from .StatsPane import StatsPane
from .UpdatePane import UpdatePane

default = "stats"


class Parameters:
    def __init__(self, master):
        self.update_image = None
        self.archive_image = None
        self.mark_image = None
        self.stats_image = None
        self.button_return = None
        self.return_image = None
        self.menu_bar = None
        self.main_frame = master.main_frame
        self.master = master
        self.button_list = None

        self.create_widgets()

        self.generate_pane(default)

    def return_window(self):
        for widgets in self.main_frame.winfo_children():
            widgets.destroy()
        TaskList.TaskList(self.master)

    def create_widgets(self):
        self.menu_bar = tk.Frame(self.main_frame)
        self.menu_bar.pack(fill="both")

        # Functions hovering buttons
        def on_enter(button):
            button.config(bg='#CFCFCF')

        def on_leave(button):
            button.config(bg='SystemButtonFace')

        def button_clicked(key_button):
            for key, val in self.button_list.items():
                if key != key_button:
                    self.button_list[key].bind("<Leave>", lambda e, button=self.button_list[key]: on_leave(button))
                    self.button_list[key].config(bg='SystemButtonFace')
            self.generate_pane(key_button)

        self.return_image = tk.PhotoImage(file='../data/images/return.PNG')
        self.button_return = tk.Button(self.menu_bar, image=self.return_image, command=lambda: self.return_window(),
                                       width=30, height=30, borderwidth=0)
        self.button_return.grid(row=0, column=0, sticky="w")

        self.button_return.bind("<Enter>", lambda e: on_enter(self.button_return))
        self.button_return.bind("<Leave>", lambda e: on_leave(self.button_return))

        self.stats_image = tk.PhotoImage(file='../data/images/stats.png')
        self.mark_image = tk.PhotoImage(file='../data/images/mark.png')
        self.archive_image = tk.PhotoImage(file='../data/images/archive.png')
        self.update_image = tk.PhotoImage(file='../data/images/update.png')

        images_list = {"stats": self.stats_image, "mark": self.mark_image, "archive": self.archive_image,
                       "update": self.update_image}
        pane_list = ["stats", "mark", "archive", "update"]
        self.button_list = {}
        col = 1

        for i in pane_list:
            self.button_list[i] = tk.Button(self.menu_bar, image=images_list[i],
                                            command=lambda key_button=i: button_clicked(key_button),
                                            width=30, height=30, borderwidth=0)
            self.button_list[i].grid(row=0, column=col, sticky="e")

            self.button_list[i].bind("<Enter>", lambda e, button=self.button_list[i]: on_enter(button))
            self.button_list[i].bind("<Leave>", lambda e, button=self.button_list[i]: on_leave(button))
            col += 1

        self.menu_bar.grid_columnconfigure(1, weight=2)

    def generate_pane(self, value):
        # self.master.unbind("<Configure>")
        for widgets in self.main_frame.winfo_children():
            if widgets != self.menu_bar:
                widgets.destroy()
        self.button_list[value].unbind('<Leave>')
        self.button_list[value].config(bg='#CFCFCF')

        global default
        default = value

        if value == "mark":
            MarkManagerPane(self.master)
        elif value == "stats":
            StatsPane(self.master)
        elif value == "archive":
            ArchiveListPane(self.master)
        elif value == "update":
            UpdatePane(self.master)
