import os
import subprocess


def export_lyx_to_tex(lyx_path, tex_output_path):
    """
    Exports a LyX file to LaTeX (.tex).
    Suppress 'New binding...' warnings by redirecting stderr to DEVNULL.
    """
    subprocess.run(
        [
            "/Applications/LyX 2.app/Contents/MacOS/lyx",
            "--export", "latex",
            lyx_path
        ],
        check=True,
        stdout=subprocess.DEVNULL,  # Hide standard output
        stderr=subprocess.DEVNULL  # Hide warnings and errors
    )

    # After running LyX, a .tex file with the same base name
    # should be created in the same directory as lyx_path.
    # We rename/move it to tex_output_path if needed:
    original_tex_path = os.path.splitext(lyx_path)[0] + ".tex"
    if os.path.abspath(original_tex_path) != os.path.abspath(tex_output_path):
        if os.path.exists(original_tex_path):
            os.rename(original_tex_path, tex_output_path)
        else:
            raise FileNotFoundError(
                f"Expected .tex file not found: {original_tex_path}")


def replace_unwanted_characters(text):
    """
    Removes or replaces unwanted characters from the text.
    Add more lines as needed.
    """
    # Example: Remove 'Ł' and any other characters you might want to strip out
    text = text.replace('Ł', '')
    # text = text.replace('Ò', '')
    return text


def convert_tex_cp1255_to_utf8(cp1255_tex_path, utf8_tex_path):
    """
    Reads a .tex file encoded in CP1255, removes stray characters, and writes it in UTF-8.
    """
    with open(cp1255_tex_path, 'r', encoding='cp1255', errors='replace') as f:
        content = f.read()

    # Remove or replace any unwanted characters
    content = replace_unwanted_characters(content)

    # Write the result as UTF-8
    with open(utf8_tex_path, 'w', encoding='utf-8') as f:
        f.write(content)


def convert_tex_to_markdown(utf8_tex_path, md_output_path):
    """
    Converts a UTF-8 .tex file to Markdown using Pandoc, without YAML front matter.
    Suppress warnings if needed by redirecting stderr.
    """
    subprocess.run(
        [
            "/opt/homebrew/bin/pandoc",
            utf8_tex_path,
            "--from=latex",
            "--to=markdown",
            "--wrap=none",
            "-o", md_output_path
        ],
        check=True,
        stdout=subprocess.DEVNULL,  # Hide standard output from Pandoc
        stderr=subprocess.DEVNULL  # Hide warnings/errors from Pandoc
    )


def cleanup_files(*file_paths):
    """
    Deletes any files that exist in the file_paths list.
    """
    for path in file_paths:
        if os.path.exists(path):
            os.remove(path)


def lyx_to_markdown(lyx_file_path, output_directory):
    """
    Main pipeline:
    1. Export LyX (.lyx) to LaTeX (.tex) (CP1255 encoded).
    2. Convert the CP1255 .tex file to a UTF-8 .tex file.
    3. Convert that UTF-8 .tex to Markdown (no extra YAML front matter).
    4. Clean up intermediate files.
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
        # 1. Export LyX -> TeX
        export_lyx_to_tex(lyx_file_path, cp1255_tex_path)

        # 2. Convert .tex from CP1255 to UTF-8
        convert_tex_cp1255_to_utf8(cp1255_tex_path, utf8_tex_path)

        # 3. Convert UTF-8 .tex -> Markdown (no front matter)
        convert_tex_to_markdown(utf8_tex_path, markdown_file_path)

        print(f"Markdown file created: {markdown_file_path}")
        return markdown_file_path

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Conversion failed: {e}")

    finally:
        # 4. Clean up any intermediate files
        cleanup_files(cp1255_tex_path, utf8_tex_path)


def main():
    # Example usage:
    lyx_file = "/Users/yonatan.levko/PycharmProjects/lyxtomarkdown/newfile2.lyx"
    output_dir = "/Users/yonatan.levko/PycharmProjects/lyxtomarkdown"

    try:
        markdown_file = lyx_to_markdown(lyx_file, output_dir)
        print(f"Markdown file successfully created at: {markdown_file}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()
