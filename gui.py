import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading

from converter.lyx_converter import LyxConverter
from config.config_manager import ConfigManager
from logging_utils.logger import Logger
from logging_utils.error_handler import ErrorHandler

from gui_frames.config_frame import ConfigFrame
from gui_frames.io_frame import IOFrame
from gui_frames.action_frame import ActionFrame
from gui_frames.status_frame import StatusFrame

class LyxConverterApp(tk.Tk):
    """The main controller class for the LyX to Markdown converter GUI."""
    def __init__(self):
        super().__init__()
        self.title("LyX to Markdown Converter")
        self.geometry("700x500")
        self.minsize(650, 500)

        # --- Setup Core Components ---
        self.logger = Logger()
        self.error_handler = ErrorHandler(self.logger)
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
        self.logger.info("Application started and configuration loaded.")

        self._setup_theme()
        self._create_widgets()

        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _setup_theme(self):
        style = ttk.Style(self)
        try:
            style.theme_use('aqua')
        except tk.TclError:
            style.theme_use('default')

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)

        self.config_frame = ConfigFrame(main_frame, self, self.config["paths"])
        self.config_frame.pack(fill="x", pady=5)

        self.io_frame = IOFrame(main_frame, self, self.config["paths"])
        self.io_frame.pack(fill="x", pady=10)

        self.action_frame = ActionFrame(main_frame, self._start_conversion_thread)
        self.action_frame.pack(fill="x", pady=10)

        self.status_frame = StatusFrame(main_frame, "Status")
        self.status_frame.pack(fill="both", expand=True, pady=5)

    def browse_executable(self, selector):
        path = filedialog.askopenfilename()
        if path:
            self.logger.info(f"Selected executable path: {path}")
            selector.set(path)

    def browse_lyx_file(self, selector):
        path = filedialog.askopenfilename(filetypes=[("LyX files", "*.lyx"), ("All files", "*.*")]
        )
        if path:
            self.logger.info(f"Selected input LyX file: {path}")
            selector.set(path)
            self.io_frame.set_output_dir(os.path.dirname(path))

    def browse_output_dir(self, selector):
        path = filedialog.askdirectory()
        if path:
            self.logger.info(f"Selected output directory: {path}")
            selector.set(path)

    def _start_conversion_thread(self):
        self.action_frame.set_button_state("disabled")
        self.status_frame.clear()
        self.logger.info("Conversion process started by user.")

        thread = threading.Thread(target=self._run_conversion)
        thread.daemon = True
        thread.start()

    def _run_conversion(self):
        config_paths = self.config_frame.get_paths()
        io_paths = self.io_frame.get_paths()
        
        lyx_file = io_paths.get("last_lyx_file")
        output_dir = io_paths.get("last_output_dir")

        if not all([config_paths.get("lyx_executable"), config_paths.get("pandoc_executable"), lyx_file, output_dir]):
            self.error_handler.handle_exception(ValueError("All paths must be specified."))
            messagebox.showerror("Error", "All paths must be specified.")
            self.action_frame.set_button_state("normal")
            return

        try:
            self.status_frame.log(f"Starting conversion for: {os.path.basename(lyx_file)}...")
            self.logger.info(f"Conversion arguments: {config_paths}, {io_paths}")

            # Use the new LyxConverter class
            converter = LyxConverter(
                lyx_executable=config_paths["lyx_executable"],
                pandoc_executable=config_paths["pandoc_executable"],
                logger=self.logger
            )
            markdown_file = converter.convert(lyx_file_path=lyx_file, output_directory=output_dir)

            self.status_frame.log(f"\nSuccess! Markdown file created at:")
            self.status_frame.log(markdown_file)
            self.logger.info(f"Conversion successful. Output: {markdown_file}")
            messagebox.showinfo("Success", "Conversion completed successfully!")

        except Exception as e:
            user_message = self.error_handler.handle_exception(e)
            self.status_frame.log(f"\nAn error occurred. See logs/app.log for details.")
            messagebox.showerror("Conversion Failed", user_message)
        finally:
            self.action_frame.set_button_state("normal")

    def _on_closing(self):
        """Handles saving the config on window close."""
        self.logger.info("Application closing, saving configuration.")
        config_paths = self.config_frame.get_paths()
        io_paths = self.io_frame.get_paths()
        self.config["paths"] = {**config_paths, **io_paths}
        self.config_manager.save_config(self.config)
        self.destroy()

if __name__ == "__main__":
    app = LyxConverterApp()
    app.mainloop()
