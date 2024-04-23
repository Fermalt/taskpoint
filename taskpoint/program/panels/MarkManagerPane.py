import tkinter as tk

from tkinter import font
from taskpoint.program.utils import Database
from taskpoint.program.utils.GenericFunctions import scroll_binding


class MarkManagerPane:
    def __init__(self, master):
        self.main_frame = master.main_frame
        self.master = master
        self.create_widgets()

    def create_widgets(self):

        createMarkBar = tk.Frame(self.main_frame)
        createMarkBar.pack(pady=(10, 10))

        def validate_input(text):
            if len(text) <= 20:
                return True
            else:
                return False

        validate_length = createMarkBar.register(validate_input)

        newMarkInput = tk.Entry(createMarkBar, font=font.Font(size=14), validate="key", validatecommand=(
            validate_length, '%P'))
        newMarkInput.insert(0, "Nouvelle catégorie")
        newMarkInput.configure(fg="gray")
        newMarkInput.bind("<FocusIn>", lambda event: on_entry_click(newMarkInput, "Nouvelle catégorie"))
        newMarkInput.bind("<FocusOut>", lambda event: on_focusout(newMarkInput, "Nouvelle catégorie"))
        newMarkInput.grid(row=0, column=0, padx=10)

        newMarkButton = tk.Button(createMarkBar, text="Valider", font=font.Font(size=14), command=lambda: add_mark())
        newMarkButton.grid(row=0, column=1)

        canvas = tk.Canvas(self.main_frame)

        scrollbar = tk.Scrollbar(canvas, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="both")
        canvas.unbind_all("<MouseWheel>")
        buttons_frame = tk.Frame(canvas)
        buttons_frame.pack(fill="both", expand=True)
        buttons_frame.update_idletasks()
        canvas.create_window((0, 0), window=buttons_frame, width=buttons_frame.winfo_width())

        def on_entry_click(entry, message):
            if entry.get() == message:
                entry.delete(0, tk.END)
                print(entry.get())
            entry.config(fg="black")

        def on_focusout(entry, message):
            if entry.get() == "":
                entry.insert(0, message)
                entry.config(fg="gray")

        def add_mark():
            mark = newMarkInput.get()
            if mark != "" and mark != "Nouvelle catégorie":
                for widget in buttons_frame.winfo_children():
                    widget.destroy()
                Database.add_mark(mark)
                marks = Database.get_all_marks()
                adding_marks(marks)

        marks = Database.get_all_marks()

        def delete_mark(id_mark, index):
            Database.delete_mark_from_id(id_mark)
            markDict[index].destroy()
            buttons_frame.update_idletasks()
            scroll_binding(canvas, scrollbar, buttons_frame)

        markDict = {}

        def adding_marks(marks):
            j = 0
            self.ImageDelete = tk.PhotoImage(file='../data/images/delete.png')
            for i, row in enumerate(marks):
                markDict[j] = row[0]
                markDict[j] = tk.Frame(buttons_frame, borderwidth=1, bg='lightgray', border=1)
                markDict[j].grid(row=i, column=0, sticky="ew", pady=3, padx=5)
                buttons_frame.grid_columnconfigure(0, weight=1)
                markDict[j].update_idletasks()
                label1 = tk.Label(markDict[j], text=row[1], bg='lightgray', font=("Calibri", 16))
                label1.grid(row=0, column=0, sticky="w")
                deleteButton = tk.Button(markDict[j], image=self.ImageDelete,
                                         command=lambda id_mark=row[0], index=j: delete_mark(id_mark, index), width=30,
                                         height=30)
                deleteButton.grid(row=0, column=1, sticky="e")
                markDict[j].grid_columnconfigure(0, weight=1)
                markDict[j].update_idletasks()
                j += 1

            buttons_frame.update_idletasks()
            scroll_binding(canvas, scrollbar, buttons_frame)


        adding_marks(marks)
        canvas.configure(scrollregion=canvas.bbox("all"))
        buttons_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
