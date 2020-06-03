import os
import tkinter as tk
from tkinter import ttk, filedialog
from pubsub import pub
from pandas import DataFrame, read_csv

ENTRY_FONT = ("Calibri", 10)
ENTRY_WIDTH = 50


class Form(tk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 1, 2, 3), weight=1)

        self.file_path_1 = tk.StringVar()
        file_entry_1 = tk.Entry(
            self,
            state="disabled",
            textvariable=self.file_path_1,
            width=ENTRY_WIDTH,
            font=ENTRY_FONT
        )
        file_entry_1.grid(row=0, column=0, sticky="EW", padx=(10, 5), pady=(10, 10))
        file_button_1 = ttk.Button(
            self,
            text="File 1",
            cursor="hand2",
            command=lambda: self.file_path_1.set(self.browse_files())
        )
        file_button_1.grid(row=0, column=1, padx=(0, 10))
        file_button_1.focus()

        self.file_path_2 = tk.StringVar()
        file_entry_2 = tk.Entry(
            self,
            state="disabled",
            textvariable=self.file_path_2,
            width=ENTRY_WIDTH,
            font=ENTRY_FONT
        )
        file_entry_2.grid(row=1, column=0, sticky="EW", padx=(10, 5), pady=(10, 10))
        file_button_2 = ttk.Button(
            self,
            text="File 2",
            cursor="hand2",
            command=lambda: self.file_path_2.set(self.browse_files())
        )
        file_button_2.grid(row=1, column=1, padx=(0, 10))

        right_weight_frame = ttk.Frame(self)
        right_weight_frame.columnconfigure(1, weight=1)
        right_weight_frame.grid(row=2, column=0, sticky="EW", columnspan=2)

        self.drop_duplicates = tk.IntVar()
        duplicates_check = ttk.Checkbutton(
            right_weight_frame,
            text="Remove duplicates",
            variable=self.drop_duplicates,
        )
        duplicates_check.grid(row=0, column=0, sticky="W", padx=(10, 5), pady=(10, 10))

        self.subset = tk.StringVar()
        subset_entry = tk.Entry(
            right_weight_frame,
            textvariable=self.subset,
            width=ENTRY_WIDTH,
            font=ENTRY_FONT
        )
        subset_entry.grid(row=0, column=1, padx=(10, 10), pady=(10, 10))

        self.sort_flag = tk.IntVar()
        sort_check = ttk.Checkbutton(
            right_weight_frame,
            text="Sort",
            variable=self.sort_flag
        )
        sort_check.grid(row=1, column=0, sticky="W", padx=(10, 5), pady=(10, 10))

        self.sort_columns = tk.StringVar()
        sort_columns_entry = tk.Entry(
            right_weight_frame,
            textvariable=self.sort_columns,
            width=ENTRY_WIDTH,
            font=ENTRY_FONT
        )
        sort_columns_entry.grid(row=1, column=1, padx=(10, 10), pady=(10, 10))

        self.output_file_path = tk.StringVar()
        output_file_entry = tk.Entry(
            self,
            state="disabled",
            textvariable=self.output_file_path,
            width=ENTRY_WIDTH,
            font=ENTRY_FONT
        )
        output_file_entry.grid(row=3, column=0, sticky="EW", padx=(10, 5), pady=(10, 10))

        save_as_button = ttk.Button(
            self,
            text="Save As",
            cursor="hand2",
            command=lambda: self.output_file_path.set(self.save_as_filename())
        )
        save_as_button.grid(row=3, column=1, padx=(0, 10))

        button_frame = ttk.Frame(self)
        button_frame.grid(row=4, column=0, sticky="EWS", columnspan=2)
        button_frame.columnconfigure((0, 1), weight=1)

        clear_button = ttk.Button(
            button_frame,
            text="Clear",
            cursor="hand2",
            command=self.clear_form
        )

        merge_button = ttk.Button(
            button_frame,
            text="Merge",
            cursor="hand2",
            command=self.merge
        )
        clear_button.grid(row=0, column=0, sticky="WS", padx=(10, 0), pady=(10, 10))
        merge_button.grid(row=0, column=1, sticky="ES", padx=(0, 10), pady=(10, 10))

    def browse_files(self):
        documents_path = os.path.expanduser("~")
        file_path = filedialog.askopenfilename(
            parent=self,
            title="Select csv file",
            initialdir=documents_path,
            filetypes=[("CSV File", "*.csv")]
        )
        return file_path

    def save_as_filename(self):
        documents_path = os.path.expanduser("~")
        file_path = filedialog.asksaveasfilename(
            parent=self,
            title="Select csv file",
            initialdir=documents_path,
            filetypes=[("CSV File", "*.csv")],
            defaultextension=".csv"
        )
        return file_path

    def clear_form(self):
        self.file_path_1.set("")
        self.file_path_2.set("")
        self.subset.set("")
        self.sort_columns.set("")
        self.output_file_path.set("")
        self.drop_duplicates.set(0)
        self.sort_flag.set(0)

    def merge(self):
        print("Merge!")

        df = read_csv(self.file_path_1.get()).append(read_csv(self.file_path_2.get()), ignore_index=True)

        subset_keys = [key.strip() for key in self.subset.get().split(",")]
        sort_keys = [key.strip() for key in self.sort_columns.get().split(",")]

        if self.drop_duplicates.get():
            df.drop_duplicates(subset=subset_keys, inplace=True, ignore_index=True)

        if self.sort_flag.get():
            df.sort_values(by=sort_keys, inplace=True, ignore_index=True)

        df.to_csv(self.output_file_path.get(), index=False)

        pub.sendMessage("merged", output=self.output_file_path.get())
        pub.sendMessage("show_frame", key="reader")
