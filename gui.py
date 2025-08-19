import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading

# Import the refactored conversion function from main.py
from main import lyx_to_markdown

# --- Color Scheme ---
BG_COLOR = "#3c3c3c"  # Dark gray
FG_COLOR = "#ffffff"  # White
BTN_BG_COLOR = "#555555"
BTN_FG_COLOR = "#ffffff"
ENTRY_BG_COLOR = "#555555"
ENTRY_FG_COLOR = "#ffffff"

class LyxConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LyX to Markdown Converter")
        self.geometry("700x450")
        self.minsize(650, 450)

        # --- Style Configuration ---
        style = ttk.Style(self)
        style.theme_use('clam')

        # Configure root window color
        self.configure(bg=BG_COLOR)

        # Configure widget styles
        style.configure('TFrame', background=BG_COLOR)
        style.configure('TLabel', background=BG_COLOR, foreground=FG_COLOR, padding=5)
        style.configure('TLabelframe', background=BG_COLOR, bordercolor=FG_COLOR)
        style.configure('TLabelframe.Label', background=BG_COLOR, foreground=FG_COLOR, font=('Helvetica', 12, 'bold'))

        # Style for Entry widgets
        style.configure('TEntry', fieldbackground=ENTRY_BG_COLOR, foreground=ENTRY_FG_COLOR, borderwidth=1, insertcolor=FG_COLOR)

        # --- Main Frame ---
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)

        # --- Configuration Frame ---
        config_frame = ttk.LabelFrame(main_frame, text="Configuration", padding="10")
        config_frame.pack(fill="x", pady=5)
        config_frame.grid_columnconfigure(1, weight=1)

        self.lyx_path = tk.StringVar(value="/Applications/LyX.app/Contents/MacOS/lyx")
        self.pandoc_path = tk.StringVar(value="/opt/homebrew/bin/pandoc")

        ttk.Label(config_frame, text="LyX Executable:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(config_frame, textvariable=self.lyx_path).grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        tk.Button(config_frame, text="Select LyX...", command=lambda: self.browse_file(self.lyx_path),
                  bg=BTN_BG_COLOR, fg=BTN_FG_COLOR, relief="raised", bd=1).grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(config_frame, text="Pandoc Executable:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(config_frame, textvariable=self.pandoc_path).grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        tk.Button(config_frame, text="Select Pandoc...", command=lambda: self.browse_file(self.pandoc_path),
                  bg=BTN_BG_COLOR, fg=BTN_FG_COLOR, relief="raised", bd=1).grid(row=1, column=2, padx=5, pady=5)

        # --- I/O Frame ---
        io_frame = ttk.LabelFrame(main_frame, text="Input & Output", padding="10")
        io_frame.pack(fill="x", pady=10)
        io_frame.grid_columnconfigure(1, weight=1)

        self.lyx_file = tk.StringVar()
        self.output_dir = tk.StringVar()

        ttk.Label(io_frame, text="Input LyX File:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(io_frame, textvariable=self.lyx_file).grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        tk.Button(io_frame, text="Select .lyx File...", command=self.browse_lyx_file,
                  bg=BTN_BG_COLOR, fg=BTN_FG_COLOR, relief="raised", bd=1).grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(io_frame, text="Output Directory:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(io_frame, textvariable=self.output_dir).grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        tk.Button(io_frame, text="Select Directory...", command=self.browse_output_dir,
                  bg=BTN_BG_COLOR, fg=BTN_FG_COLOR, relief="raised", bd=1).grid(row=1, column=2, padx=5, pady=5)

        # --- Action Frame ---
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill="x", pady=10)

        self.convert_button = tk.Button(action_frame, text="Convert to Markdown", command=self.start_conversion_thread,
                                       bg=BTN_BG_COLOR, fg=BTN_FG_COLOR, relief="raised", bd=2, font=('Helvetica', 10, 'bold'))
        self.convert_button.pack()

        # --- Status Frame ---
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.pack(fill="both", expand=True, pady=5)
        status_frame.grid_rowconfigure(0, weight=1)
        status_frame.grid_columnconfigure(0, weight=1)

        self.status_text = tk.Text(status_frame, height=6, state="disabled", relief="flat", bg=ENTRY_BG_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR)
        self.status_text.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(status_frame, orient="vertical", command=self.status_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.status_text.config(yscrollcommand=scrollbar.set)

    def browse_file(self, string_var):
        path = filedialog.askopenfilename()
        if path:
            string_var.set(path)

    def browse_lyx_file(self):
        path = filedialog.askopenfilename(filetypes=[("LyX files", "*.lyx"), ("All files", "*.*")])
        if path:
            self.lyx_file.set(path)
            self.output_dir.set(os.path.dirname(path))

    def browse_output_dir(self):
        path = filedialog.askdirectory()
        if path:
            self.output_dir.set(path)

    def log_status(self, message):
        self.status_text.config(state="normal")
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state="disabled")
        self.update_idletasks()

    def start_conversion_thread(self):
        self.convert_button.config(state="disabled")
        self.status_text.config(state="normal")
        self.status_text.delete(1.0, tk.END)
        self.status_text.config(state="disabled")

        thread = threading.Thread(target=self.run_conversion)
        thread.daemon = True
        thread.start()

    def run_conversion(self):
        lyx_exe = self.lyx_path.get()
        pandoc_exe = self.pandoc_path.get()
        lyx_file = self.lyx_file.get()
        output_dir = self.output_dir.get()

        if not all([lyx_exe, pandoc_exe, lyx_file, output_dir]):
            messagebox.showerror("Error", "All paths must be specified.")
            self.convert_button.config(state="normal")
            return

        for path, name in [(lyx_exe, "LyX"), (pandoc_exe, "Pandoc"), (lyx_file, "Input file")]:
            if not os.path.exists(path):
                messagebox.showerror("Error", f"{name} not found at the specified path:\n{path}")
                self.convert_button.config(state="normal")
                return

        try:
            self.log_status(f"Starting conversion for: {os.path.basename(lyx_file)}...")

            markdown_file = lyx_to_markdown(
                lyx_file_path=lyx_file,
                output_directory=output_dir,
                lyx_executable=lyx_exe,
                pandoc_executable=pandoc_exe
            )

            self.log_status("\nSuccess! Markdown file created at:")
            self.log_status(markdown_file)
            messagebox.showinfo("Success", "Conversion completed successfully!")

        except Exception as e:
            self.log_status(f"\nError: {e}")
            messagebox.showerror("Conversion Failed", f"An error occurred:\n{e}")
        finally:
            self.convert_button.config(state="normal")

if __name__ == "__main__":
    app = LyxConverterApp()
    app.mainloop()