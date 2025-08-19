import os
from converter.lyx_converter import LyxConverter

def main():
    """
    Example of how to run the conversion from the command line using the converter package.
    Users should update the paths below to match their system configuration.
    """
    # --- Configuration ---
    # Path to the LyX executable
    LYX_EXECUTABLE = "/Applications/LyX.app/Contents/MacOS/lyx"  # For macOS

    # Path to the Pandoc executable
    PANDOC_EXECUTABLE = "/opt/homebrew/bin/pandoc"  # For macOS with Homebrew

    # Input and output files
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
        
        # 1. Initialize the converter
        converter = LyxConverter(lyx_executable=LYX_EXECUTABLE, pandoc_executable=PANDOC_EXECUTABLE)
        
        # 2. Run the conversion
        markdown_file = converter.convert(lyx_file_path=lyx_file, output_directory=output_dir)
        
        print(f"\nFinal Markdown file successfully created at: {markdown_file}")

    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == '__main__':
    main()