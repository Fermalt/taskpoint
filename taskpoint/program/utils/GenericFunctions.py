import tkinter as tk


def scroll_binding(canvas, scrollbar, frame):
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    if canvas.winfo_height() >= frame.winfo_height():
        scrollbar.pack_forget()
        canvas.unbind_all("<MouseWheel>")
        canvas.unbind('<Enter>')
        canvas.unbind('<Leave>')
    else:
        # Active la barre de défilement
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.bind('<Enter>', lambda event: canvas.config(scrollregion=canvas.bbox("all")))

    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.yview_moveto(0.0)


class GenericFunctions:
    pass
