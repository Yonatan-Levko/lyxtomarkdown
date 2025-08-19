import os
import re
import subprocess

def export_lyx_to_tex(lyx_path, tex_output_path, lyx_executable):
    """Exports a LyX file to LaTeX (.tex) using a specified executable."""
    # Capture output to see potential errors from LyX
    result = subprocess.run(
        [lyx_executable, "--export", "latex", lyx_path],
        capture_output=True, text=True
    )

    # If LyX reports an error, raise it with the detailed message
    if result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode, result.args, 
            output=result.stdout, stderr=result.stderr
        )

    original_tex_path = os.path.splitext(lyx_path)[0] + ".tex"
    if os.path.abspath(original_tex_path) != os.path.abspath(tex_output_path):
        if os.path.exists(original_tex_path):
            os.rename(original_tex_path, tex_output_path)
        else:
            raise FileNotFoundError(
                f"Expected .tex file not found: {original_tex_path}")


def convert_tex_cp1255_to_utf8(cp1255_tex_path, utf8_tex_path):
    """Reads a .tex file in CP1255, drops unreadable bytes, and writes as UTF-8."""
    with open(cp1255_tex_path, 'r', encoding='cp1255', errors='ignore') as f:
        content = f.read()

    content = content.replace("Ł$", "$")
    content = content.replace("Ł", "")

    with open(utf8_tex_path, 'w', encoding='utf-8') as f:
        f.write(content)


def convert_tex_to_markdown(utf8_tex_path, md_output_path, pandoc_executable):
    """
    Converts a UTF-8 .tex file to Markdown using a specified Pandoc executable.
    """
    subprocess.run(
        [
            pandoc_executable,
            utf8_tex_path,
            "--from=latex",
            "--to=markdown",
            "--wrap=none",
            "-o", md_output_path
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


def cleanup_files(*file_paths):
    """Deletes any files that exist in the file_paths list."""
    for path in file_paths:
        if os.path.exists(path):
            os.remove(path)


def lyx_to_markdown(lyx_file_path, output_directory, lyx_executable, pandoc_executable):
    """
    Full conversion process from LyX to Markdown using specified executables.
    """
    if not os.path.exists(lyx_file_path):
        raise FileNotFoundError(f"LyX file not found: {lyx_file_path}")

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    base_name = os.path.splitext(os.path.basename(lyx_file_path))[0]
    cp1255_tex_path = os.path.join(output_directory, f"{base_name}.tex")
    utf8_tex_path = os.path.join(output_directory, f"{base_name}_utf8.tex")
    markdown_file_path = os.path.join(output_directory, f"{base_name}.md")

    try:
        export_lyx_to_tex(lyx_file_path, cp1255_tex_path, lyx_executable)
        convert_tex_cp1255_to_utf8(cp1255_tex_path, utf8_tex_path)
        convert_tex_to_markdown(utf8_tex_path, markdown_file_path, pandoc_executable)

        # Post-processing steps
        remove_stray_character_from_md(markdown_file_path)
        flip_parentheses_outside_math(markdown_file_path)

        print(f"Markdown file created: {markdown_file_path}")
        return markdown_file_path
    except FileNotFoundError as e:
        raise RuntimeError(f"Conversion failed: A file was not found. {e}")
    except subprocess.CalledProcessError as e:
        # Include the detailed error from the LyX command in the exception
        error_message = e.stderr or e.stdout or "No error output from command."
        raise RuntimeError(f"Conversion failed. The command '{' '.join(e.cmd)}' failed with exit code {e.returncode}.\n\nUnderlying error:\n---\n{error_message.strip()}\n---")
    finally:
        cleanup_files(cp1255_tex_path, utf8_tex_path)


def remove_stray_character_from_md(md_file, char_to_remove="Ł"):
    """
    Opens the final .md file, removes the given character everywhere, and overwrites the file.
    """
    if not os.path.exists(md_file):
        return

    with open(md_file, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    content = content.replace(char_to_remove, "")

    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(content)


MATH_PATTERN = re.compile(r'(\${1,2}.*?\${1,2})', flags=re.DOTALL)

def flip_parentheses_outside_math(md_file):
    """
    Reads the final Markdown file, splits it into math vs. non-math segments,
    flips parentheses only in the non-math segments, and overwrites the file.
    """
    if not os.path.exists(md_file):
        return

    with open(md_file, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    segments = MATH_PATTERN.split(content)

    def flip_parens(s):
        s = s.replace('(', '§').replace(')', '(').replace('§', ')')
        return s

    new_segments = []
    for seg in segments:
        if seg.startswith(') and seg.endswith('):
            new_segments.append(seg)
        else:
            new_segments.append(flip_parens(seg))

    new_content = ''.join(new_segments)

    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(new_content)


def main():
    """
    Example of how to run the conversion from the command line.
    Users should update the paths below to match their system configuration.
    """
    # --- Configuration ---
    # Path to the LyX executable
    LYX_EXECUTABLE = "/Applications/LyX.app/Contents/MacOS/lyx"  # For macOS
    # LYX_EXECUTABLE = "C:\\Program Files\\LyX 2.3\\bin\\lyx.exe"  # For Windows
    # LYX_EXECUTABLE = "/usr/bin/lyx"  # For Linux

    # Path to the Pandoc executable
    PANDOC_EXECUTABLE = "/opt/homebrew/bin/pandoc"  # For macOS with Homebrew
    # PANDOC_EXECUTABLE = "C:\\Program Files\\Pandoc\\pandoc.exe"  # For Windows
    # PANDOC_EXECUTABLE = "/usr/bin/pandoc"  # For Linux

    # Input and output files
    # Note: It's better to use absolute paths to avoid issues.
    project_dir = os.path.dirname(os.path.abspath(__file__))
    lyx_file = os.path.join(project_dir, "newfile2.lyx")
    output_dir = project_dir
    # --- End of Configuration ---

    # Verify that the executables exist
    if not os.path.exists(LYX_EXECUTABLE):
        print(f"Error: LyX executable not found at: {LYX_EXECUTABLE}")
        return
    if not os.path.exists(PANDOC_EXECUTABLE):
        print(f"Error: Pandoc executable not found at: {PANDOC_EXECUTABLE}")
        return

    try:
        print("Starting conversion...")
        markdown_file = lyx_to_markdown(
            lyx_file_path=lyx_file,
            output_directory=output_dir,
            lyx_executable=LYX_EXECUTABLE,
            pandoc_executable=PANDOC_EXECUTABLE
        )
        print(f"\nFinal Markdown file successfully created at: {markdown_file}")
    except Exception as e:
        print(f"\nAn error occurred: {e}")


if __name__ == '__main__':
    main()
