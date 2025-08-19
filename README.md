# LyX to Markdown Converter

This script converts LyX files (.lyx) to clean, readable Markdown files (.md). It is designed to handle LyX files written in Hebrew with CP1255 encoding and correctly process mathematical formulas.

The conversion is a multi-step process that uses LyX for LaTeX export and Pandoc for the final conversion to Markdown, with several cleaning and formatting steps in between.

## Features

-   Converts `.lyx` files to `.md`.
-   Handles `CP1255` (Hebrew) encoding and converts it to `UTF-8`.
-   Uses **LyX** to export to LaTeX and **Pandoc** for robust Markdown conversion.
-   Cleans up intermediate files automatically.
-   Performs post-processing on the final Markdown file to:
    -   Remove stray characters.
    -   Intelligently flip parentheses `()` in the text while ignoring parentheses within math equations (`$...$` or `$$...$$`).

## Prerequisites

This script relies on external command-line tools. You must have the following software installed on your system:

1.  **LyX**: A document processor. The script requires the LyX executable to be available. You can download it from [lyx.org](https://www.lyx.org/Download).
2.  **Pandoc**: A universal document converter. You can find installation instructions at [pandoc.org/installing.html](https://pandoc.org/installing.html). On macOS, it is easily installed with Homebrew:
    ```bash
    brew install pandoc
    ```

## Configuration

Before running the script, you need to configure the paths to your LyX installation, the Pandoc executable, and the input/output files.

Open the `main.py` file and modify the following:

1.  **LyX Executable Path**: In the `export_lyx_to_tex` function, update the path to your LyX executable.
    ```python
    # Example for macOS
    subprocess.run(
        [
            "/Applications/LyX 2.app/Contents/MacOS/lyx", # <-- UPDATE THIS PATH
            "--export", "latex",
            lyx_path
        ],
        # ...
    )
    ```

2.  **Pandoc Executable Path**: In the `convert_tex_to_markdown` function, ensure the path to `pandoc` is correct.
    ```python
    # Example for macOS with Homebrew
    subprocess.run(
        [
            "/opt/homebrew/bin/pandoc", # <-- UPDATE THIS PATH
            utf8_tex_path,
            # ...
        ],
        # ...
    )
    ```

3.  **Input and Output Files**: In the `main` function at the bottom of the script, set the path to your source `.lyx` file and the desired output directory.
    ```python
    def main():
        # UPDATE these paths for your use case
        lyx_file = "/path/to/your/document.lyx"
        output_dir = "/path/to/your/output_folder"

        # ...
    ```

## Usage

Once the configuration is complete, you can run the script from your terminal:

```bash
python main.py
```

The script will execute the conversion process and print the path to the final Markdown file upon successful completion. If an error occurs, it will be printed to the console.

## How It Works

The script performs the following sequence of operations:

1.  **Export to LaTeX**: It calls the LyX command-line tool to export the input `.lyx` file into a `.tex` file with `CP1255` encoding.
2.  **Convert Encoding**: The script reads the `.tex` file using `CP1255` encoding, performs minor text corrections, and saves it as a new `.tex` file in `UTF-8`.
3.  **Convert to Markdown**: It uses Pandoc to convert the `UTF-8`-encoded `.tex` file into a Markdown file.
4.  **Cleanup**: The intermediate `.tex` files created during the process are deleted.
5.  **Post-Processing**:
    -   Any stray "Ł" characters that may appear during encoding conversion are removed from the final `.md` file.
    -   Parentheses are flipped to correct their direction for right-to-left text, but only outside of math blocks, preserving the integrity of mathematical expressions.