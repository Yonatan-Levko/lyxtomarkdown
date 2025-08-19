import os

def cleanup_files(*file_paths, logger=None):
    """Deletes any files that exist in the file_paths list."""
    for path in file_paths:
        if os.path.exists(path):
            try:
                if logger:
                    logger.info(f"Removing intermediate file: {path}")
                os.remove(path)
            except OSError as e:
                if logger:
                    logger.error(f"Error removing file {path}: {e}")
