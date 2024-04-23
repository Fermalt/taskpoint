import tkinter as tk

from tkinter import font, messagebox, ttk
from taskpoint.program.utils import Database
from taskpoint.program.utils.GenericFunctions import scroll_binding
from . import TaskList
from . import Parameters

label_exists = False
micro_task_bar = {}
checkbox_values = []


class ModifyTask:
    global label_exists
    global checkbox_values

    def __init__(self, master, task=None, archive=None):
        self.return_image = None
        print(task)
        self.main_frame = master.main_frame
        self.master = master
        self.archive = archive
        global label_exists
        label_exists = False
        if task is None:
            self.task = ["", "", 5, "", "", 0, 0, 0, ""]
        else:
            self.task = task

        self.micro_task_bar = {}
        global checkbox_values
        self.create_widgets()

    def create_widgets(self):

        def return_task_list():
            title = title_field.get()
            task_type = type_task_selection.get()
            mark = combobox.get()
            task_id = id_label.cget("text")
            if task_type == 0:
                description = description_field.get("1.0", tk.END).rstrip('\n')
                if task_id is None or task_id == "":
                    if (title != "" and title != "Titre") or (description != "" and description != "Description"):
                        if var_selection.get() == 5:
                            messagebox.showinfo("Attention", "Aucun état n'a été défini pour la tâche")
                            return
                        Database.create_classical_task(title, var_selection.get(), task_type, mark, description)
                else:
                    Database.modify_classical_task(task_id, title, var_selection.get(), task_type, mark, description)

                for widgets in self.main_frame.winfo_children():
                    widgets.destroy()
                if self.archive is None:
                    TaskList.TaskList(self.master)
                else:
                    Parameters.Parameters(self.master)
            else:
                i = 0
                """for element in micro_task_bar:
                    micro_tasks = []
                     micro_tasks[i] = element[0]"""
                if task_id is None or task_id == "":
                    for checklist in buttons_frame.winfo_children():
                        for micro_task_barrr in buttons_frame.winfo_children():
                            print(micro_task_barrr)
                        #if isinstance(checklist, tk.Text):
                        if description is not None:
                            if (title != "" and title != "Titre") or (
                                    description != "" and description != "Description"):
                                if var_selection.get() == 5:
                                    messagebox.showinfo("Attention", "Aucun état n'a été défini pour la tâche")
                                    return
                                micro_task_dict = []
                                i = -1
                                widgetss = self.micro_task_bar[0].winfo_children()
                                values = ()
                                for element in widgetss:
                                    i += 1
                                    j = -1
                                    if i == 0:
                                        values = (checkbox_values[0].get(),)
                                    if i == 1:
                                        values = values + (element.get("1.0", tk.END).rstrip('\n'),)
                                micro_task_dict.append(values)
                                Database.create_checklist_task(title, var_selection.get(), task_type, mark,
                                                               micro_task_dict)
                else:
                    global micro_task_bar
                    checklist_canvas = micro_task_bar[0].winfo_children()
                    frame_widgets = micro_task_bar[0].winfo_children()
                    if frame_widgets is not None:
                        if title != "" and title != "Titre":
                            micro_task_dict = []
                            i = -1
                            values = ()
                            for element in frame_widgets:
                                i += 1
                                j = -1
                                if i == 0:
                                    values = (checkbox_values[0].get(),)
                                if i == 1:
                                    values = values + (element.get("1.0", tk.END).rstrip('\n'),)
                            micro_task_dict.append(values)
                            Database.modify_checklist_task(task_id, title, var_selection.get(), task_type, mark,
                                                           micro_task_dict)

                for widgets in self.main_frame.winfo_children():
                    widgets.destroy()
                if self.archive is None:
                    TaskList.TaskList(self.master)
                else:
                    title = title_field.get()

        menu_bar = tk.Frame(self.main_frame)
        menu_bar.pack(fill="both")

        # Functions hovering buttons
        def on_enter(button):
            button.config(bg='#CFCFCF')

        def on_leave(button):
            button.config(bg='SystemButtonFace')

        self.return_image = tk.PhotoImage(file='../data/images/return.PNG')
        button_return = tk.Button(menu_bar, image=self.return_image,
                                  command=return_task_list,
                                  width=30, height=30, borderwidth=0, compound=tk.CENTER)
        button_return.grid(row=0, column=0, sticky="w")
        menu_bar.grid_columnconfigure(0, weight=1)
        menu_bar.grid_columnconfigure(1, weight=1)
        menu_bar.grid_columnconfigure(2, weight=1)
        button_return.bind("<Enter>", lambda e: on_enter(button_return))
        button_return.bind("<Leave>", lambda e: on_leave(button_return))

        def create_edit_pane():

            for widgets in text_frame.winfo_children():
                widgets.destroy()

            global id_label
            global description_field
            global buttons_frame

            # Classic task type
            if type_task_selection.get() == 0:
                def on_entry_click2(entry, message):
                    if entry.get("1.0", tk.END) == message + "\n":
                        entry.delete("1.0", tk.END)
                    entry.config(fg="black")

                def on_focusout2(entry, message):
                    if entry.get("1.0", tk.END) == "\n":
                        entry.insert("1.0", message)
                        entry.config(fg="gray")

                text_scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL)
                description_field = tk.Text(text_frame, yscrollcommand=text_scrollbar.set, font=tk.font.Font(size=14),
                                            wrap="word", height=12)

                text_scrollbar.config(command=description_field.yview)
                text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

                description_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                description_field.pack()
                description_field.insert("1.0", self.task[8])
                if description_field.get("1.0", tk.END) == "\n":
                    description_field.insert("1.0", "Description")
                    description_field.configure(fg="gray")
                description_field.bind("<FocusIn>",
                                       lambda event: on_entry_click2(description_field, "Description"))
                description_field.bind("<FocusOut>", lambda event: on_focusout2(description_field, "Description"))

            # Check-list task type
            elif type_task_selection.get() == 1:
                def on_entry_click2(entry, message):
                    if entry.get("1.0", tk.END) == message + "\n":
                        entry.delete("1.0", tk.END)
                    entry.config(fg="black")

                def on_focusout2(entry, message):
                    if entry.get("1.0", tk.END) == "\n":
                        entry.insert("1.0", message)
                        entry.config(fg="gray")

                checklist_canvas = tk.Canvas(text_frame, borderwidth=0)
                checklist_canvas.pack(fill="both", expand=True)
                scrollbar = tk.Scrollbar(checklist_canvas, orient="vertical", command=checklist_canvas.yview)
                checklist_canvas.configure(yscrollcommand=scrollbar.set)

                scrollbar.pack(side="right", fill="both")
                buttons_frame = tk.Frame(checklist_canvas, width=checklist_canvas.winfo_width(), borderwidth=0)
                buttons_frame.pack(fill="both", expand=True)
                buttons_frame.update_idletasks()
                checklist_canvas.create_window((0, 0), window=buttons_frame, width=buttons_frame.winfo_width())

                #tasks_canvas = tk.Canvas()

                global i
                i = -1

                def add_check_task(first):
                    global i
                    global checkbox_values
                    global micro_task_bar
                    if first == "first":
                        checklists = Database.get_all_checklists_of_task(self.task[0])
                        print("checklist" + str(checklists))
                        for i in range(0, len(checklists)):
                            checkbox_values.insert(i, tk.BooleanVar())
                            micro_task_bar[i] = tk.Frame(buttons_frame, bg="green")
                            micro_task_bar[i].pack(fill="both")
                            # micro_task_scrollbar = tk.Scrollbar(micro_task_bar, orient=tk.VERTICAL)
                            checkbox = tk.Checkbutton(micro_task_bar[i], font=tk.font.Font(size=14),
                                                      variable=checkbox_values[i])
                            description_field = tk.Text(micro_task_bar[i], font=tk.font.Font(size=14),
                                                        wrap="word", height=2, width=10)

                            # description_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                            # description_field.pack()
                            checkbox.grid(row=0, column=0)
                            checkbox.configure(fg="gray")
                            checkbox.bind("<FocusIn>",
                                          lambda event: on_entry_click2(description_field, "Description"))
                            checkbox.bind("<FocusOut>", lambda event: on_focusout2(description_field, "Description"))

                            description_field.grid(row=0, column=1)
                            description_field.columnconfigure(1, weight=2)
                            # description_field.insert("1.0", self.task[5][0])
                            if description_field.get("1.0", tk.END) == "\n":
                                description_field.insert("1.0", "Description")
                                description_field.configure(fg="gray")
                            description_field.bind("<FocusIn>",
                                                   lambda event: on_entry_click2(description_field, "Description"))
                            description_field.bind("<FocusOut>",
                                                   lambda event: on_focusout2(description_field, "Description"))
                    i += 1
                    # text_frame.configure(yscrollcommand=scrollbar.set)
                    # text_frame.pack(side="top", fill="both", expand=True)

                    checkbox_values.insert(i, tk.BooleanVar())
                    micro_task_bar[i] = tk.Frame(buttons_frame, bg="green")
                    micro_task_bar[i].pack(fill="both")
                    # micro_task_scrollbar = tk.Scrollbar(micro_task_bar, orient=tk.VERTICAL)
                    checkbox = tk.Checkbutton(micro_task_bar[i], font=tk.font.Font(size=14),
                                              variable=checkbox_values[i])
                    description_field = tk.Text(micro_task_bar[i], font=tk.font.Font(size=14),
                                                wrap="word", height=2, width=10)

                    # description_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                    # description_field.pack()
                    checkbox.grid(row=0, column=0)
                    checkbox.configure(fg="gray")
                    checkbox.bind("<FocusIn>",
                                  lambda event: on_entry_click2(description_field, "Description"))
                    checkbox.bind("<FocusOut>", lambda event: on_focusout2(description_field, "Description"))

                    description_field.grid(row=0, column=1)
                    description_field.columnconfigure(1, weight=2)
                    # description_field.insert("1.0", self.task[5][0])
                    if description_field.get("1.0", tk.END) == "\n":
                        description_field.insert("1.0", "Description")
                        description_field.configure(fg="gray")
                    description_field.bind("<FocusIn>",
                                           lambda event: on_entry_click2(description_field, "Description"))
                    description_field.bind("<FocusOut>", lambda event: on_focusout2(description_field, "Description"))

                    def delete_checklist(checklist_task):
                        checklist_task.destroy()

                    delete_button = tk.Button(micro_task_bar[i], text="Supprimer",
                                              command=lambda checklist=micro_task_bar[i]:
                                              delete_checklist(checklist))
                    delete_button.grid(row=0, column=2)

                    # micro_task_scrollbar.grid(row=0, column=2, sticky="e")

                    add_task_button.pack()

                    #checklist_canvas.configure(scrollregion=checklist_canvas.bbox("all"))
                    #checklist_canvas.bind("<Configure>", lambda e: checklist_canvas.configure(
                    #    scrollregion=checklist_canvas.bbox("all")))
                    # scroll_binding(text_frame, text_scrollbar, text_frame)

                    #checklist_canvas.yview_moveto(0.0)

                    scroll_binding(checklist_canvas, scrollbar, text_frame)

                # text_scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL)
                add_task_button = tk.Button(text_frame, text="Ajouter une tâche", command=lambda: add_check_task("second"),
                                            font=font.Font(size=13))
                add_check_task("first")

                # text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

                add_task_button.pack()

            global label_exists
            if not label_exists:
                id_label = tk.Label(self.main_frame, text=self.task[0])
                id_label.pack(side="right", anchor="se")
                label_exists = True

        type_task_selection = tk.IntVar()

        type_task_selection.set(0)
        if self.task[3] != "":
            type_task_selection.set(self.task[3])

        task_type_bloc = tk.Frame(menu_bar)
        task_type_bloc.grid(row=0, column=1)
        task_type_bloc.columnconfigure(0, weight=1)
        task_type_bloc.columnconfigure(1, weight=1)

        classic_task_button = tk.Radiobutton(task_type_bloc, text="Tâche",
                                             variable=type_task_selection,
                                             value=0,
                                             indicatoron=False,
                                             font=font.Font(size=14),
                                             command=create_edit_pane)
        classic_task_button.grid(row=0, column=0, padx=(0, 5))

        checklist_task_button = tk.Radiobutton(task_type_bloc, text="Check-Liste",
                                               variable=type_task_selection,
                                               value=1,
                                               indicatoron=False,
                                               font=font.Font(size=14),
                                               command=create_edit_pane)
        checklist_task_button.grid(row=0, column=1, padx=(0, 5))

        state_buttons_bar = tk.Frame(self.main_frame)
        state_buttons_bar.pack(pady=(10, 10))

        var_selection = tk.IntVar()
        var_selection.set(5)
        if self.task[2] != "":
            var_selection.set(self.task[2])

        states_name = ["A faire", "En cours", "Terminé", "Autres"]
        states_color = ["#ff9f22", "#F3E700", "#76DD00", "#AAAAAA"]
        buttons_states_dict = {}
        for i in range(0, 4):
            buttons_states_dict[i] = tk.Radiobutton(state_buttons_bar, variable=var_selection, text=states_name[i],
                                                    value=i,
                                                    indicatoron=False,
                                                    font=font.Font(size=14), selectcolor=states_color[i])
            buttons_states_dict[i].grid(row=0, column=i + 1, padx=(0, 5))

        # Create the Listbox
        options_list = ['']
        marks_data = Database.get_all_marks()
        for mark in marks_data:
            options_list.append(mark[1])
        default_value = Database.get_mark_from_id(self.task[3])
        if default_value is None:
            default_value = ['']

        combobox = ttk.Combobox(self.main_frame, state='readonly', font=font.Font(size=14))
        combobox['values'] = options_list
        combobox.set(default_value[0])
        combobox.pack(pady=5)

        def on_entry_click(entry, message):
            if entry.get() == message:
                entry.delete(0, tk.END)
            entry.config(fg="black")

        def on_focusout(entry, message):
            if entry.get() == "":
                entry.insert(0, message)
                entry.config(fg="gray")

        title_field = tk.Entry(self.main_frame, width=self.main_frame.winfo_width(), font=font.Font(size=14))
        title_field.insert(0, self.task[1])
        if title_field.get() == "":
            title_field.insert(0, "Titre")
            title_field.configure(fg="gray")
        title_field.bind("<FocusIn>", lambda event: on_entry_click(title_field, "Titre"))
        title_field.bind("<FocusOut>", lambda event: on_focusout(title_field, "Titre"))
        title_field.pack()

        text_frame = tk.Frame(self.main_frame)
        text_frame.pack(fill="both", expand=True)

        create_edit_pane()
