import tkinter as tk

from tkinter import font
from taskpoint.program.utils import Database
from taskpoint.program.utils.GenericFunctions import scroll_binding


class StatsPane:
    def __init__(self, master):
        self.main_frame = master.main_frame

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
        # canvas.create_window((0, 0), window=buttons_frame, width=buttons_frame.winfo_width())

        canvas.unbind_all("<MouseWheel>")
        total_task = 0
        number = Database.get_number_from_state(0)
        total_task += number[0]
        stats1 = tk.Label(buttons_frame, text="Tâches à faire : " + str(number[0]), font=font.Font(size=14))
        stats1.grid(row=0, column=0)
        buttons_frame.grid_columnconfigure(0, weight=1)
        number = Database.get_number_from_state(1)
        taskInProgress = number[0]
        total_task += number[0]
        stats2 = tk.Label(buttons_frame, text="Tâches en cours : " + str(number[0]), font=font.Font(size=14))
        stats2.grid(row=1, column=0)
        number = Database.get_number_from_state(2)
        total_task += number[0]
        stats3 = tk.Label(buttons_frame, text="Tâches réalisées : " + str(number[0]), font=font.Font(size=14))
        stats3.grid(row=2, column=0)

        if total_task != 0:
            progress_bar = tk.Frame(buttons_frame, borderwidth=1, bg="gray", height=30, width=200)
            task_inProgress_value = (taskInProgress * 100) / total_task
            task_inProgress_value = task_inProgress_value * 200 / 100
            progression = tk.Frame(progress_bar, bg="#FCEC52", height=30, width=task_inProgress_value)
            progress_bar.grid(row=3, column=0, pady=(20, 0))
            progression.place(relx=0, rely=0)
            task_done_value = (number[0] * 100) / total_task
            task_done_value = task_done_value * 200 / 100
            done = tk.Frame(progress_bar, bg="#76DD00", height=30, width=task_done_value)
            progress_bar.grid(row=3, column=0, pady=(20, 0))
            done.place(relx=0, rely=0)

        graphs_canvas = tk.Canvas(buttons_frame, borderwidth=1, width=400, height=250)
        scrollbar_graphs = tk.Scrollbar(buttons_frame, orient="horizontal", bg="blue", command=graphs_canvas.xview)
        graphs_canvas.configure(xscrollcommand=scrollbar_graphs.set)
        graphs_canvas.grid(row=4, column=0, pady=(20, 0), sticky="n")
        scrollbar_graphs.grid(row=5, column=0, sticky="ew", padx=(50, 50))
        graphs_canvas.update_idletasks()
        graphs_canvas.pack_propagate(False)

        container = tk.Frame(graphs_canvas, bg="gray", borderwidth=1, height=250)
        container.grid(row=0, column=0)
        graphs_canvas.grid_rowconfigure(0, weight=1)
        graphs_canvas.grid_columnconfigure(0, weight=1)
        container.update_idletasks()
        graphs_canvas.create_window((0, 0), window=container, anchor=tk.S)

        marks_number_tmp = Database.get_all_marks()
        marks_number = []
        for i in range(0, len(marks_number_tmp)):
            if Database.get_number_from_state(2, marks_number_tmp[i][1])[0] + \
                    Database.get_number_from_state(0, marks_number_tmp[i][1])[0] + \
                    Database.get_number_from_state(1, marks_number_tmp[i][1])[0] != 0:
                marks_number.append(marks_number_tmp[i])
        marks_forms_dict = {}
        marks_label_dict = {}
        colors_list = ["blue", "green", "yellow", "cyan", "magenta", "red",
                       "orange", "purple", "pink", "brown", "gray", "indigo"]
        for i in range(0, len(marks_number)):
            total_tasks = Database.get_number_from_state(2, marks_number[i][1])[0] + \
                          Database.get_number_from_state(0, marks_number[i][1])[0] + \
                          Database.get_number_from_state(1, marks_number[i][1])[0]
            if total_tasks != 0:
                if len(marks_number) < 4:
                    task_width = 400 / len(marks_number)
                    container.config(width=400)
                else:
                    task_width = 120
                    container.config(width=120 * len(marks_number))
                tasks_done = Database.get_number_from_state(2, marks_number[i][1])[0]
                marks_forms_dict[i] = tk.Frame(container, bg=colors_list[i], width=task_width,
                                               height=250 * tasks_done / total_tasks)
                marks_forms_dict[i].pack(pady=0, side=tk.LEFT, padx=0, anchor="s")
                if 250 * tasks_done / total_tasks == 0:
                    marks_forms_dict[i].pack_forget()
                marks_forms_dict[i].pack_propagate(False)
                marks_label_dict[i] = tk.Label(marks_forms_dict[i], text=marks_number[i][1])
                marks_label_dict[i].pack(pady=marks_forms_dict[i].winfo_height() -
                                               marks_label_dict[i].winfo_height())

        buttons_frame.update_idletasks()
        container.pack_propagate(False)
        container.config(height=250)

        scroll_binding(canvas, scrollbar, buttons_frame)
        canvas.configure(scrollregion=canvas.bbox("all"))

        scroll_binding(graphs_canvas, scrollbar_graphs, container)
        graphs_canvas.configure(scrollregion=graphs_canvas.bbox("all"))

        graphs_canvas.xview_moveto(0.0)
