# LyX to Markdown Converter

This project provides a tool with a graphical user interface (GUI) to convert LyX files (.lyx) to clean, readable Markdown files (.md). It is designed to handle LyX files written in Hebrew with CP1255 encoding and correctly process mathematical formulas.

The conversion is a multi-step process that uses LyX for LaTeX export and Pandoc for the final conversion to Markdown, with several cleaning and formatting steps in between.

## Features

-   **Graphical User Interface** for easy operation.
-   Converts `.lyx` files to `.md`.
-   Handles `CP1255` (Hebrew) encoding and converts it to `UTF-8`.
-   Uses **LyX** to export to LaTeX and **Pandoc** for robust Markdown conversion.
-   Cleans up intermediate files automatically.
-   Performs post-processing on the final Markdown file to:
    -   Remove stray characters.
    -   Intelligently flip parentheses `()` in the text while ignoring parentheses within math equations (`$...$` or `$$...$$`).

## Prerequisites

This tool relies on external command-line programs. You must have the following software installed on your system:

1.  **LyX**: A document processor. You can download it from [lyx.org](https://www.lyx.org/Download).
2.  **Pandoc**: A universal document converter. You can find installation instructions at [pandoc.org/installing.html](https://pandoc.org/installing.html). On macOS, it is easily installed with Homebrew:
    ```bash
    brew install pandoc
    ```

## Usage (GUI Mode)

The recommended way to use this tool is via the graphical interface.

### 1. Run the Application

Navigate to the project directory in your terminal and run:

```bash
python gui.py
```

This will launch the application window.

### 2. Configure Paths

-   **LyX Executable**: The application will try to find a default path for the LyX executable. If it's incorrect, click "Browse..." to locate it on your system.
-   **Pandoc Executable**: Similarly, confirm the path to the Pandoc executable.

### 3. Select Files

-   **Input LyX File**: Click "Browse..." to select the `.lyx` file you want to convert.
-   **Output Directory**: Choose the folder where you want to save the converted `.md` file. This will default to the same directory as the input file.

### 4. Convert

Click the "Convert to Markdown" button. The status panel at the bottom will show the progress, and a message will appear upon completion.

## Advanced Usage (Command-Line)

For advanced users or for automation, you can run the conversion directly from the command line.

### Configuration

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

### Run the Script

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
    -   Any stray "Ł" characters that may appear during encoding conversion are removed from the final `.md` file.
    -   Parentheses are flipped to correct their direction for right-to-left text, but only outside of math blocks, preserving the integrity of mathematical expressions.
