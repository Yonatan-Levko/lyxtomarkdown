import tkinter as tk
from tkinter import ttk
from .path_selector import PathSelector

class IOFrame(ttk.LabelFrame):
    """Frame for selecting input and output paths."""
    def __init__(self, parent, controller, default_paths):
        super().__init__(parent, text="Input & Output", padding="10")

        self.lyx_file_selector = PathSelector(
            self, "Input LyX File:", 
            controller.browse_lyx_file, 
            default_paths.get("last_lyx_file", "")
        )
        self.lyx_file_selector.pack(fill="x", pady=2)

        self.output_dir_selector = PathSelector(
            self, "Output Directory:", 
            controller.browse_output_dir, 
            default_paths.get("last_output_dir", "")
        )
        self.output_dir_selector.pack(fill="x", pady=2)

    def get_paths(self):
        return {
            "last_lyx_file": self.lyx_file_selector.get(),
            "last_output_dir": self.output_dir_selector.get()
        }
    
    def set_output_dir(self, path):
        self.output_dir_selector.set(path)
