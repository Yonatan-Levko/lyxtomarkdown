import os
import re
import subprocess

def export_lyx_to_tex(lyx_path, tex_output_path):
    """Exports a LyX file to LaTeX (.tex)."""
    subprocess.run(
        [
            "/Applications/LyX 2.app/Contents/MacOS/lyx",
            "--export", "latex",
            lyx_path
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
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

    # Example: minimal text fix before writing
    content = content.replace("Ł$", "$")  # if you sometimes see Ł before $
    content = content.replace("Ł", "")    # remove standalone Ł

    with open(utf8_tex_path, 'w', encoding='utf-8') as f:
        f.write(content)


def convert_tex_to_markdown(utf8_tex_path, md_output_path):
    """
    Converts a UTF-8 .tex file to Markdown using Pandoc, without YAML front matter.
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
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


def cleanup_files(*file_paths):
    """Deletes any files that exist in the file_paths list."""
    for path in file_paths:
        if os.path.exists(path):
            os.remove(path)


def lyx_to_markdown(lyx_file_path, output_directory):
    """
    1. Export LyX (.lyx) to LaTeX (.tex) (CP1255).
    2. Convert .tex from CP1255 to UTF-8.
    3. Convert UTF-8 .tex to Markdown.
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

        # 2. Convert CP1255 TeX -> UTF-8 TeX
        convert_tex_cp1255_to_utf8(cp1255_tex_path, utf8_tex_path)

        # 3. Convert UTF-8 TeX -> Markdown
        convert_tex_to_markdown(utf8_tex_path, markdown_file_path)

        print(f"Markdown file created: {markdown_file_path}")
        return markdown_file_path
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Conversion failed: {e}")
    finally:
        # 4. Clean up intermediate files
        cleanup_files(cp1255_tex_path, utf8_tex_path)


def remove_stray_character_from_md(md_file, char_to_remove="Ł"):
    """
    Opens the final .md file, removes the given character everywhere, and overwrites the file.
    """
    if not os.path.exists(md_file):
        return  # Nothing to do if file doesn't exist

    with open(md_file, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # Remove the unwanted character
    content = content.replace(char_to_remove, "")

    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(content)


########################################################################
# New function to flip parentheses only outside of math mode
########################################################################
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

    # Split by math segments: [non-math, $math$, non-math, $$math$$, ...]
    segments = MATH_PATTERN.split(content)

    def flip_parens(s):
        """
        Flips '(' and ')' in a string:
          - '(' becomes ')'
          - ')' becomes '('
        """
        # 1) Temporarily replace '(' with a placeholder
        s = s.replace('(', '§')
        # 2) Replace ')' with '('
        s = s.replace(')', '(')
        # 3) Replace placeholder '§' with ')'
        s = s.replace('§', ')')
        return s

    new_segments = []
    for seg in segments:
        # If it's a math segment (starts and ends with $ or $$),
        # we keep it exactly as is.
        if (seg.startswith('$') and seg.endswith('$')):
            new_segments.append(seg)
        else:
            # Non-math segment: flip parentheses
            flipped = flip_parens(seg)
            new_segments.append(flipped)

    new_content = ''.join(new_segments)

    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(new_content)


def main():
    # Example usage
    lyx_file = "/Users/yonatan.levko/PycharmProjects/lyxtomarkdown/newfile2.lyx"
    output_dir = "/Users/yonatan.levko/PycharmProjects/lyxtomarkdown"

    try:
        # 1. Convert LyX to Markdown
        markdown_file = lyx_to_markdown(lyx_file, output_dir)

        # 2. Remove stray 'Ł' from the final Markdown file
        remove_stray_character_from_md(markdown_file, "Ł")

        # 3. Flip parentheses only outside math mode
        flip_parentheses_outside_math(markdown_file)

        print(f"Final Markdown file successfully created at: {markdown_file}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()
