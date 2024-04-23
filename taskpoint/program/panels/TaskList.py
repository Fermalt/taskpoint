import tkinter as tk

from tkinter import font, ttk
from . import Parameters
from . import ModifyTask
from taskpoint.program.utils import Database
from taskpoint.program.utils.GenericFunctions import scroll_binding

VERSION = "v3.0-040923"


class TaskList:
    def __init__(self, master):
        self.parameters_image = None
        self.new_task_image = None
        self.main_frame = master.main_frame
        self.master = master

        self.create_widgets()

    def create_widgets(self):

        def parameters():
            self.master.unbind("<Configure>")
            canvas.unbind_all("<MouseWheel>")
            for widgets in self.main_frame.winfo_children():
                widgets.destroy()
            Parameters.Parameters(self.master)

        def modify_task(task_id=None):
            self.master.unbind("<Configure>")
            canvas.unbind_all("<MouseWheel>")
            for widgets in self.main_frame.winfo_children():
                widgets.destroy()
            if task_id is not None:
                task = Database.get_global_task_details_from_id(task_id)
                if task[3] == '0':
                    task = task + Database.get_classical_task_details_from_id(task_id)
                elif task[3] == '1':
                    print(Database.get_checklist_task_details_from_id(task_id))
                ModifyTask.ModifyTask(self.master, task)
            else:
                ModifyTask.ModifyTask(self.master)

        def new_task():
            from .ModifyTask import ModifyTask
            self.master.unbind("<Configure>")
            canvas.unbind_all("<MouseWheel>")
            for widgets in self.main_frame.winfo_children():
                widgets.destroy()
            ModifyTask(self.master)

        # Menu bar generation
        menu_bar = tk.Frame(self.main_frame)
        menu_bar.pack(fill="both")

        # Functions hovering buttons
        def on_enter(button):
            button.config(bg='#CFCFCF')

        def on_leave(button):
            button.config(bg='SystemButtonFace')

        self.new_task_image = tk.PhotoImage(file='../data/images/newTask.png')
        button_new_task = tk.Button(menu_bar, image=self.new_task_image, width=30, height=30,
                                    command=new_task,
                                    borderwidth=0, compound=tk.CENTER)
        button_new_task.grid(row=0, column=0, sticky="w")
        menu_bar.grid_columnconfigure(0, weight=3)
        button_new_task.bind("<Enter>", lambda e: on_enter(button_new_task))
        button_new_task.bind("<Leave>", lambda e: on_leave(button_new_task))

        self.parameters_image = tk.PhotoImage(file='../data/images/parameters.png')
        button_parameters = tk.Button(menu_bar, image=self.parameters_image,
                                      command=lambda: parameters(),
                                      width=30, height=30, borderwidth=0, compound=tk.CENTER)
        button_parameters.grid(row=0, column=6, sticky="e")
        menu_bar.grid_columnconfigure(6, weight=3)
        button_parameters.bind("<Enter>", lambda e: on_enter(button_parameters))
        button_parameters.bind("<Leave>", lambda e: on_leave(button_parameters))

        # Filters tasks
        def filters_selected():
            for widget in tasks_frame.winfo_children():
                widget.destroy()
            states_id_list = [0, 1, 2, 3]
            for key, states in states_dict.items():
                if states.get():
                    states_id_list.append(key)
                else:
                    states_id_list.remove(key)

            current_value = combobox_var.get()
            matching_values = [value for value in options_list if value.startswith(current_value)]
            combobox['values'] = matching_values
            if not states_id_list:
                states_id_list = [0, 1, 2, 3]
            if current_value == "":
                tasks = Database.get_all_tasks(states_id_list, "nothing")
            else:
                tasks = Database.get_all_tasks(states_id_list, current_value)
            adding_tasks(tasks)

        # States buttons
        states_name = ["A faire", "En cours", "Terminé", "Autres"]
        states_dict = {0: tk.BooleanVar(), 1: tk.BooleanVar(), 2: tk.BooleanVar(), 3: tk.BooleanVar()}
        button_states_dict = {}
        for i in range(0, 4):
            button_states_dict[i] = tk.Checkbutton(menu_bar, text=states_name[i], variable=states_dict[i],
                                                   command=filters_selected,
                                                   font=font.Font(size=12))
            button_states_dict[i].grid(row=0, column=i + 1)
            menu_bar.grid_columnconfigure(i + 1, weight=1)

        options_list = ['']
        marks_data = Database.get_all_marks()
        for mark in marks_data:
            options_list.append(mark[1])
        combobox_var = tk.StringVar()
        combobox = ttk.Combobox(self.main_frame, textvariable=combobox_var, font=font.Font(size=14))
        combobox['values'] = options_list
        combobox.bind("<KeyRelease>", lambda e: filters_selected())
        combobox.bind("<Key>", lambda e: filters_selected())
        combobox.bind('<<ComboboxSelected>>', lambda e: filters_selected())
        combobox.pack(pady=5)

        # Tasks list generation
        canvas = tk.Canvas(self.main_frame)
        scrollbar = tk.Scrollbar(canvas, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="top", fill="both", expand=True)
        scrollbar.pack(side="right", fill="both")

        tasks_frame = tk.Frame(canvas, width=canvas.winfo_width(), height=canvas.winfo_height())
        tasks_frame.pack(fill="both", expand=True)
        tasks_frame.update_idletasks()
        canvas.create_window((0, 0), window=tasks_frame, width=tasks_frame.winfo_width())

        def adding_tasks(tasks):

            def frame_action(id_task):
                modify_task(id_task)

            """def release_grab(event):
                if event.widget == self.master:
                    self.master.grab_release()

            self.master.bind("<Button-1>", release_grab)"""

            def open_small_frame(id_task):
                small_frame = tk.Frame(self.main_frame, width=200, height=100, bg='white')
                small_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

                def delete_task():
                    Database.delete_task_from_id(id_task)
                    small_frame.destroy()
                    filters_selected()

                def archive_task():
                    Database.archive_task(id_task)
                    small_frame.destroy()
                    filters_selected()

                def close_small_frame():
                    small_frame.destroy()

                button_archive = tk.Button(small_frame, text="Archiver",
                                           command=archive_task)
                button_archive.pack(pady=5)

                button_delete = tk.Button(small_frame, text="Supprimer",
                                          command=delete_task)
                button_delete.pack(pady=5)

                button_close = tk.Button(small_frame, text="Fermer", command=close_small_frame)
                button_close.pack(pady=5)

                # self.master.bind("<Button-1>", lambda event: close_small_frame(event, small_frame))
                small_frame.grab_set()

            self.moreImage = tk.PhotoImage(file='../data/images/more.png')

            button_style = ttk.Style()
            button_style.configure('Custom.TButton', relief='flat', borderwidth=0)

            button_dict = {}
            j = 0
            for i, row in enumerate(tasks):
                color = 'white'
                match row[2]:
                    case 0:
                        color = '#ff9f22'
                    case 1:
                        color = '#F3E700'
                    case 2:
                        color = '#76DD00'

                button_style.configure('Custom.TButton', bg=color)
                button_dict[j] = row[0]
                button_dict[j] = tk.Frame(tasks_frame, borderwidth=1, bg=color, border=1)
                button_dict[j].bind("<Button-1>", lambda e, id=row[0]: frame_action(id))
                button_dict[j].grid(row=i, column=0, sticky="ew", pady=3, padx=5)
                tasks_frame.grid_columnconfigure(0, weight=1)
                label1 = tk.Label(button_dict[j], text=row[1], font=("Calibri", 16), bg=color)
                button_more = ttk.Button(button_dict[j], image=self.moreImage, style='Custom.TButton',
                                         command=lambda id_task=row[0]: open_small_frame(id_task))
                button_more.grid(row=0, column=1, sticky="e")
                label1.grid(row=0, column=0, sticky="w")
                label1.bind("<Button-1>", lambda e, id_task=row[0]: frame_action(id_task))
                button_dict[j].grid_columnconfigure(0, weight=1)
                j += 1

            tasks_frame.update_idletasks()

            canvas.configure(scrollregion=canvas.bbox("all"))
            tasks_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            scroll_binding(canvas, scrollbar, tasks_frame)

        # Download the tasks in a text file
        def version_click(event):
            Database.download_database()
            print("Base de données sauvegardée !")

        version_tab = tk.Label(self.main_frame, text=VERSION)
        version_tab.pack(side=tk.RIGHT)
        version_tab.bind("<Button-1>", version_click)
        filters_selected()
