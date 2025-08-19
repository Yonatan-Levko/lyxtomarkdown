import os
import subprocess

from .file_utils import cleanup_files
from .postprocess import remove_stray_character_from_md, flip_parentheses_outside_math

class LyxConverter:
    """Handles the full conversion process from a LyX file to Markdown."""
    def __init__(self, lyx_executable, pandoc_executable):
        """
        Initializes the converter with paths to required executables.

        Args:
            lyx_executable (str): The path to the LyX executable.
            pandoc_executable (str): The path to the Pandoc executable.
        """
        self.lyx_executable = lyx_executable
        self.pandoc_executable = pandoc_executable

    def convert(self, lyx_file_path, output_directory):
        """
        Executes the full conversion process.

        Args:
            lyx_file_path (str): The absolute path to the input .lyx file.
            output_directory (str): The directory to save the output and intermediate files.

        Returns:
            str: The path to the final Markdown file.
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
            self._export_to_tex(lyx_file_path, cp1255_tex_path)
            self._convert_encoding_to_utf8(cp1255_tex_path, utf8_tex_path)
            self._convert_tex_to_markdown(utf8_tex_path, markdown_file_path)

            # Post-processing steps
            remove_stray_character_from_md(markdown_file_path)
            flip_parentheses_outside_math(markdown_file_path)

            return markdown_file_path
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            # The exception is re-raised to be handled by the caller (e.g., the GUI)
            raise RuntimeError(f"Conversion failed: {e}")
        finally:
            cleanup_files(cp1255_tex_path, utf8_tex_path)

    def _export_to_tex(self, lyx_path, tex_output_path):
        result = subprocess.run(
            [self.lyx_executable, "--export", "latex", lyx_path],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            raise subprocess.CalledProcessError(
                result.returncode, result.args, output=result.stdout, stderr=result.stderr
            )
        
        original_tex_path = os.path.splitext(lyx_path)[0] + ".tex"
        if os.path.abspath(original_tex_path) != os.path.abspath(tex_output_path):
            if os.path.exists(original_tex_path):
                os.rename(original_tex_path, tex_output_path)
            else:
                raise FileNotFoundError(f"Expected .tex file not found: {original_tex_path}")

    def _convert_encoding_to_utf8(self, cp1255_path, utf8_path):
        with open(cp1255_path, 'r', encoding='cp1255', errors='ignore') as f:
            content = f.read()
        content = content.replace("Ł$", "$").replace("Ł", "")
        with open(utf8_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def _convert_tex_to_markdown(self, tex_path, md_path):
        subprocess.run(
            [self.pandoc_executable, tex_path, "--from=latex", "--to=markdown", "--wrap=none", "-o", md_path],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
