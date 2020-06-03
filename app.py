import tkinter as tk
from tkinter import ttk
from pubsub import pub

from frames.form import Form
from frames.reader import Reader


class CsvMerger(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("CSV File Merge")
        # self.geometry("400x300")
        # self.resizable(False, False)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        container = ttk.Frame(self)
        container.grid()

        self.frames = dict()

        form_frame = Form(container)
        form_frame.grid(row=0, column=0, sticky="NSEW")

        reader_frame = Reader(container)
        reader_frame.grid(row=0, column=0, sticky="NSEW")

        self.frames["form"] = form_frame
        self.frames["reader"] = reader_frame

        pub.subscribe(self.show_frame, "show_frame")

        self.show_frame("form")

    def show_frame(self, key):
        frame = self.frames[key]
        frame.tkraise()


app = CsvMerger()
app.mainloop()