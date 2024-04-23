import tkinter as tk

from tkinter import font, ttk

from . import ModifyTask
from taskpoint.program.utils import Database
from taskpoint.program.utils.GenericFunctions import scroll_binding


class ArchiveListPane:
    def __init__(self, master):
        self.main_frame = master.main_frame
        self.master = master

        self.create_widgets()

    def create_widgets(self):

        def modify_task(task_id):
            canvas.unbind_all("<MouseWheel>")
            for widgets in self.master.main_frame.winfo_children():
                widgets.destroy()

            task = Database.get_global_task_details_from_id(task_id)
            if task[5] == '0':
                task = task + Database.get_classical_task_details_from_id(task_id)
            elif task[5] == '1':
                print(Database.get_checklist_task_details_from_id(task_id))
            ModifyTask.ModifyTask(self.master, task, True)

        # Tasks list generation
        canvas = tk.Canvas(self.main_frame)
        scrollbar = ttk.Scrollbar(canvas, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="both")

        buttons_frame = tk.Frame(canvas, width=canvas.winfo_width())
        buttons_frame.pack(fill="both", expand=True)
        buttons_frame.update_idletasks()
        canvas.create_window((0, 0), window=buttons_frame, width=buttons_frame.winfo_width())

        def frame_action(button):
            modify_task(button)

        def release_grab(event):
            # Relâcher la capture lorsque vous cliquez en dehors du frame
            if event.widget == self.master:
                self.master.grab_release()

        self.master.main_frame.bind("<Button-1>", release_grab)

        def open_small_frame(id_task):
            small_frame = tk.Frame(self.main_frame.master, width=200, height=100, bg='white')
            small_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

            def close_small_frame():
                small_frame.destroy()

            def unarchive():
                Database.unarchive_task(id_task)
                for widget in buttons_frame.winfo_children():
                    widget.destroy()
                small_frame.destroy()
                control_archives()

            def delete_task():
                for widgets in buttons_frame.winfo_children():
                    widgets.destroy()
                Database.delete_task_from_id(id_task)
                small_frame.destroy()
                control_archives()

            button_unarchive = tk.Button(small_frame, text="Désarchiver",
                                         command=unarchive)
            button_unarchive.pack(pady=5)

            button_delete = tk.Button(small_frame, text="Supprimer",
                                      command=delete_task)
            button_delete.pack(pady=5)
            button_close = tk.Button(small_frame, text="Fermer", command=close_small_frame)
            button_close.pack(pady=5)

            # Configure the root window to bind mouse click events
            # self.master.bind("<Button-1>", lambda event: close_small_frame(event, small_frame))
            small_frame.grab_set()

        def control_archives():
            tasks = Database.get_all_archived_tasks()
            if len(tasks) != 0:
                adding_tasks(tasks)
            else:
                text_vide = tk.Label(canvas, text='Aucune archive n\'a été ajoutée.', font=font.Font(size=12))
                text_vide.pack()

            scroll_binding(canvas, scrollbar, buttons_frame)

        def adding_tasks(tasks):
            self.moreImage = tk.PhotoImage(file='../data/images/more.png')

            button_style = ttk.Style()
            button_style.configure('Custom.TButton', relief='flat', borderwidth=0)
            button_dict = {}
            j = 0
            for i, row in enumerate(tasks):
                color = 'white'
                button_style.configure('Custom.TButton', bg=color)
                button_dict[j] = row[0]
                button_dict[j] = tk.Frame(buttons_frame, borderwidth=1, bg=color, border=1)
                button_dict[j].bind("<Button-1>", lambda e, id_task=row[0]: frame_action(id_task))
                button_dict[j].grid(row=i, column=0, sticky="ew", pady=3, padx=5)
                buttons_frame.grid_columnconfigure(0, weight=1)
                label1 = tk.Label(button_dict[j], text=row[1], font=("Calibri", 16), bg=color)
                buttonMore = ttk.Button(button_dict[j], image=self.moreImage, style='Custom.TButton',
                                        command=lambda task_id=row[0]: open_small_frame(task_id))
                buttonMore.grid(row=0, column=1, sticky="e")
                label1.grid(row=0, column=0, sticky="w")
                label1.bind("<Button-1>", lambda e, id_task=row[0]: frame_action(id_task))
                button_dict[j].grid_columnconfigure(0, weight=1)
                j += 1

            buttons_frame.update_idletasks()

        control_archives()

        scroll_binding(canvas, scrollbar, buttons_frame)

        buttons_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
