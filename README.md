# LyX-to-Markdown Converter

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Pandoc](https://img.shields.io/badge/pandoc-required-brightgreen.svg)](https://pandoc.org/)
[![LyX](https://img.shields.io/badge/LyX-required-orange.svg)](https://www.lyx.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A user-friendly tool with a graphical user interface (GUI) to convert LyX (`.lyx`) files into clean, readable Markdown (`.md`) files. It is specifically designed to handle LyX files written in Hebrew with CP1255 encoding and correctly process mathematical formulas.

The conversion is a multi-step process that leverages LyX for LaTeX export and Pandoc for the final conversion to Markdown, with several cleaning and formatting steps in between.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [GUI Mode](#gui-mode)
  - [Command-Line Mode](#command-line-mode)
- [How It Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Graphical User Interface (GUI)** for easy and intuitive operation.
- Converts **`.lyx`** files to **`.md`**.
- Handles **CP1255 (Hebrew)** encoding and converts it to **UTF-8**.
- Uses **LyX** to export to LaTeX and **Pandoc** for robust Markdown conversion.
- **Automatic cleanup** of intermediate files.
- **Post-processes** the final Markdown file to:
  - Remove stray characters.
  - Intelligently flip parentheses `()` in the text while ignoring those within math equations (`$...$` or `$$...$$`).

## Project Structure

```
lyxtomarkdown/
├───.venv/                  # Virtual environment
├───config/                 # Configuration files
│   ├───config_manager.py   # Manages app configuration
│   └───settings.py         # App settings
├───converter/              # Core conversion logic
│   ├───file_utils.py       # File utilities
│   ├───lyx_converter.py    # Main conversion logic
│   └───postprocess.py      # Post-processing scripts
├───gui_frames/             # GUI frame components
│   ├───action_frame.py     # Frame for conversion actions
│   ├───config_frame.py     # Frame for app configuration
│   ├───io_frame.py         # Frame for file input/output
│   ├───path_selector.py    # Path selection widget
│   └───status_frame.py     # Frame for status updates
├───logging_utils/          # Logging utilities
│   ├───error_handler.py    # Error handling
│   └───logger.py           # Logger configuration
├───logs/                   # Log files
├───gui.py                  # Main GUI application entry point
├───main.py                 # Command-line application entry point
└───README.md               # This file
```

## Prerequisites

This tool relies on external command-line programs. You must have the following software installed on your system:

1.  **LyX**: A document processor. Download it from [lyx.org](https://www.lyx.org/Download).
2.  **Pandoc**: A universal document converter. Find installation instructions at [pandoc.org/installing.html](https://pandoc.org/installing.html).

On macOS, you can easily install Pandoc with Homebrew:
```bash
brew install pandoc
```

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/lyxtomarkdown.git
    cd lyxtomarkdown
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the required Python packages:**
    *(Currently, this project has no external Python dependencies, but it is good practice to work in a virtual environment.)*

## Usage

### GUI Mode

The recommended way to use this tool is via its graphical interface.

1.  **Run the Application:**
    Navigate to the project directory in your terminal and run:
    ```bash
    python gui.py
    ```
    This will launch the application window.

2.  **Configure Paths:**
    -   **LyX Executable**: The application will attempt to find the default path for the LyX executable. If it's incorrect, click **"Browse..."** to locate it on your system.
    -   **Pandoc Executable**: Similarly, confirm the path to the Pandoc executable.

3.  **Select Files:**
    -   **Input LyX File**: Click **"Browse..."** to select the `.lyx` file you want to convert.
    -   **Output Directory**: Choose the folder where you want to save the converted `.md` file. This defaults to the same directory as the input file.

4.  **Convert:**
    Click the **"Convert to Markdown"** button. The status panel at the bottom will show the progress, and a message will appear upon completion.

### Command-Line Mode

For advanced users or for automation, you can run the conversion directly from the command line.

1.  **Configuration:**
    Open the `main.py` file and modify the configuration variables at the bottom of the script to match the paths on your system:
    ```python
    # --- Configuration ---
    LYX_EXECUTABLE = "/Applications/LyX.app/Contents/MacOS/lyx"  # Update this
    PANDOC_EXECUTABLE = "/opt/homebrew/bin/pandoc"      # Update this

    # Input and output files
    lyx_file = "/path/to/your/document.lyx"             # Update this
    output_dir = "/path/to/your/output_folder"         # Update this
    # --- End of Configuration ---
    ```

2.  **Run the Script:**
    Once configured, run the script from your terminal:
    ```bash
    python main.py
    ```

## How It Works

The script performs the following sequence of operations:

1.  **Export to LaTeX**: It calls the LyX command-line tool to export the input `.lyx` file into a `.tex` file with `CP1255` encoding.
2.  **Convert Encoding**: The script reads the `.tex` file using `CP1255` encoding, performs minor text corrections, and saves it as a new `.tex` file in `UTF-8`.
3.  **Convert to Markdown**: It uses Pandoc to convert the `UTF-8`-encoded `.tex` file into a Markdown file.
4.  **Cleanup**: The intermediate `.tex` files created during the process are deleted.
5.  **Post-Processing**:
    -   Any stray "Ł" characters that may appear during encoding conversion are removed.
    -   Parentheses are flipped to correct their direction for right-to-left text, but only outside of math blocks, preserving the integrity of mathematical expressions.

## Contributing

Contributions are welcome! If you have suggestions for improvements, please open an issue or submit a pull request.

1.  **Fork the repository.**
2.  **Create a new branch:** `git checkout -b feature/your-feature-name`
3.  **Make your changes and commit them:** `git commit -m 'Add some feature'`
4.  **Push to the branch:** `git push origin feature/your-feature-name`
5.  **Submit a pull request.**

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.