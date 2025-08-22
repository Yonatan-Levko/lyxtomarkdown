import logging
from logging.handlers import RotatingFileHandler
import os

class Logger:
    """A centralized logger for the application."""
    def __init__(self, name='LyxConverterApp', log_file='app.log', log_level=logging.INFO, console_level=logging.INFO):
        """
        Initializes the logger.

        Args:
            name (str): The name of the logger.
            log_file (str): The name of the log file.
            log_level (int): The logging level for the file.
            console_level (int): The logging level for the console.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        # Prevent duplicate handlers if this class is instantiated multiple times
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # --- Log Directory ---
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        log_path = os.path.join(log_dir, log_file)

        # --- File Handler ---
        # Rotate logs, keeping 5 files of 1MB each.
        file_handler = RotatingFileHandler(
            log_path, maxBytes=1*1024*1024, backupCount=5
        )
        file_handler.setLevel(log_level)

        # --- Console Handler ---
        console_handler = logging.StreamHandler()
        console_handler.setLevel(console_level)

        # --- Formatter ---
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # --- Add Handlers ---
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, message):
        """Logs an info-level message."""
        self.logger.info(message)

    def warning(self, message):
        """Logs a warning-level message."""
        self.logger.warning(message)

    def error(self, message, exc_info=False):
        """Logs an error-level message."""
        self.logger.error(message, exc_info=exc_info)

    def critical(self, message, exc_info=False):
        """Logs a critical-level message."""
        self.logger.critical(message, exc_info=exc_info)
