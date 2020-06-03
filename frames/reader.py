import tkinter as tk
import csv
from tkinter import ttk
from pubsub import pub


class Reader(tk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        button_frame = ttk.Frame(self)
        button_frame.grid(row=0, column=0, sticky="EW")
        back_button = ttk.Button(
            button_frame,
            text="← Back",
            cursor="hand2",
            command=lambda: pub.sendMessage("show_frame", key="form")
        )
        back_button.grid(row=0, column=0, sticky="W", padx=(5, 0), pady=(5, 10))

        # Use a tree view to simulate a table layout
        # use show="headings" to hide the tree column, #0
        self.tree = ttk.Treeview(self, selectmode="browse", show="headings")
        self.tree.grid(row=1, column=0, sticky="NSEW", padx=(5, 5), pady=(5, 5))

        # create our X and Y scrollbars and link their command back to the tree view
        scroll_y = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scroll_y.grid(row=1, column=1, sticky="NS")
        scroll_x = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        scroll_x.grid(row=2, column=0, sticky="EW")

        self.tree["yscrollcommand"] = scroll_y.set
        self.tree["xscrollcommand"] = scroll_x.set

        # subscribe to PubSub messages for 'merged' with a output argument
        pub.subscribe(self.update_tree, "merged")

    def update_tree(self, output):
        # clear all the existing children from the tree
        self.tree.delete(*self.tree.get_children())

        # open our CSV file
        with open(output, newline="") as csvfile:
            csv_reader = csv.reader(csvfile)

            # set the tree column identifiers to be the same as the CSV header row
            header = next(csv_reader)
            self.tree["columns"] = header

            # set the text value of the column heading and its anchor
            # column is identified by its identifier set above hence f"{column}"
            for column in header:
                self.tree.heading(f"{column}", text=column, anchor="w")

            # for each data row in the CSV file, insert into the tree
            # the first argument is an empty string "" to signify that this is a top level item
            # the second argument is a 0 because there are no children so all items go at the front of their
            # respective lists
            for row in csv_reader:
                self.tree.insert("", 0, values=row)


