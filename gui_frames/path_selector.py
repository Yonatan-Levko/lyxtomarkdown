import tkinter as tk
from tkinter import ttk

class PathSelector(ttk.Frame):
    """A reusable widget for selecting a file or directory path."""
    def __init__(self, parent, label_text, browse_command, default_path=""):
        super().__init__(parent, padding=(0, 5))
        self.path = tk.StringVar(value=default_path)

        ttk.Label(self, text=label_text).grid(row=0, column=0, sticky="w", padx=(0, 5))
        ttk.Entry(self, textvariable=self.path).grid(row=0, column=1, sticky="ew", padx=5)
        # The browse_command is now a callback that receives this instance
        tk.Button(self, text="Browse...", command=lambda: browse_command(self)).grid(row=0, column=2, padx=(5, 0))

        self.grid_columnconfigure(1, weight=1)

    def get(self):
        return self.path.get()

    def set(self, path):
        self.path.set(path)
