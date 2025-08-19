import tkinter as tk
from tkinter import ttk

class StatusFrame(ttk.LabelFrame):
    """A frame for displaying status messages with a scrollbar."""
    def __init__(self, parent, text):
        super().__init__(parent, text=text, padding="10")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.text_widget = tk.Text(self, height=6, state="disabled", relief="flat",
                                   borderwidth=1)
        self.text_widget.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.text_widget.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.text_widget.config(yscrollcommand=scrollbar.set)

    def log(self, message):
        self.text_widget.config(state="normal")
        self.text_widget.insert(tk.END, message + "\n")
        self.text_widget.see(tk.END)
        self.text_widget.config(state="disabled")
        self.update_idletasks()

    def clear(self):
        self.text_widget.config(state="normal")
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.config(state="disabled")
