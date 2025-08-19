import tkinter as tk
from tkinter import ttk

class ActionFrame(ttk.Frame):
    """Frame for the main action buttons."""
    def __init__(self, parent, convert_command):
        super().__init__(parent, padding=(0, 10))

        self.convert_button = tk.Button(self, text="Convert to Markdown", command=convert_command)
        self.convert_button.pack()

    def set_button_state(self, state):
        self.convert_button.config(state=state)
