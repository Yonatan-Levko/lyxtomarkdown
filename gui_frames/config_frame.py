import tkinter as tk
from tkinter import ttk
from .path_selector import PathSelector

class ConfigFrame(ttk.LabelFrame):
    """Frame for configuring LyX and Pandoc executable paths."""
    def __init__(self, parent, controller, default_paths):
        super().__init__(parent, text="Configuration", padding="10")

        self.lyx_path_selector = PathSelector(
            self, "LyX Executable:", 
            controller.browse_executable, 
            default_paths.get("lyx_executable", "")
        )
        self.lyx_path_selector.pack(fill="x", pady=2)

        self.pandoc_path_selector = PathSelector(
            self, "Pandoc Executable:", 
            controller.browse_executable, 
            default_paths.get("pandoc_executable", "")
        )
        self.pandoc_path_selector.pack(fill="x", pady=2)

    def get_paths(self):
        return {
            "lyx_executable": self.lyx_path_selector.get(),
            "pandoc_executable": self.pandoc_path_selector.get()
        }
