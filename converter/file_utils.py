import os

def cleanup_files(*file_paths):
    """Deletes any files that exist in the file_paths list."""
    for path in file_paths:
        if os.path.exists(path):
            try:
                os.remove(path)
            except OSError as e:
                # This can be connected to a logger in the future
                print(f"Error removing file {path}: {e}")
