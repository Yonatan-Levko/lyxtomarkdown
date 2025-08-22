import os
from converter.lyx_converter import LyxConverter
from logging_utils.logger import Logger

def main():
    """
    Example of how to run the conversion from the command line using the converter package.
    Users should update the paths below to match their system configuration.
    """
    # --- Setup Logging ---
    logger = Logger()

    # --- Configuration ---
    LYX_EXECUTABLE = "/Applications/LyX 2.app/Contents/MacOS/lyx"  # For macOS
    PANDOC_EXECUTABLE = "/opt/homebrew/bin/pandoc"  # For macOS with Homebrew

    project_dir = os.path.dirname(os.path.abspath(__file__))
    lyx_file = os.path.join(project_dir, "newfile2.lyx")
    output_dir = project_dir
    # --- End of Configuration ---

    if not os.path.exists(LYX_EXECUTABLE):
        logger.error(f"LyX executable not found at: {LYX_EXECUTABLE}")
        return
    if not os.path.exists(PANDOC_EXECUTABLE):
        logger.error(f"Pandoc executable not found at: {PANDOC_EXECUTABLE}")
        return

    try:
        logger.info("Starting command-line conversion...")
        
        converter = LyxConverter(
            lyx_executable=LYX_EXECUTABLE, 
            pandoc_executable=PANDOC_EXECUTABLE, 
            logger=logger
        )
        
        markdown_file = converter.convert(lyx_file_path=lyx_file, output_directory=output_dir)
        
        logger.info(f"Conversion successful. Output at: {markdown_file}")
        print(f"\nConversion successful. Output at: {markdown_file}")

    except Exception as e:
        logger.error(f"An error occurred during command-line conversion: {e}", exc_info=True)
        print(f"\nAn error occurred: {e}")

if __name__ == '__main__':
    main()
