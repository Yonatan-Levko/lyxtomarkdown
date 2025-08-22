import traceback
from .logger import Logger

class ErrorHandler:
    """Handles exception logging and provides user-friendly messages."""
    def __init__(self, logger: Logger):
        """
        Initializes the error handler.

        Args:
            logger (Logger): An instance of the Logger class.
        """
        self.logger = logger

    def handle_exception(self, exception: Exception, user_message: str = None) -> str:
        """
        Logs a detailed exception and returns a user-friendly message.

        Args:
            exception (Exception): The exception that was caught.
            user_message (str, optional): A custom message to show the user. 
                                          If None, a generic message is used.

        Returns:
            str: A user-friendly error message.
        """
        # Log the full traceback
        detailed_error = traceback.format_exc()
        self.logger.error(f"An exception occurred: {exception}\n{detailed_error}")

        # Prepare the message for the user
        if user_message:
            return user_message
        
        return f"An unexpected error occurred: {exception}\n\nPlease check logs/app.log for detailed information."

