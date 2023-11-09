class Logger:
    """Logs messages to console in different colors."""

    @staticmethod
    def log_pink(message):
        """Logs a message to console in pink color."""
        print(f"\033[95m{message}\033[00m")

    @staticmethod
    def log_yellow(message):
        """Logs a message to console in yellow color."""
        print(f"\033[93m{message}\033[00m")

    @staticmethod
    def log_green(message):
        """Logs a message to console in green color.""" ""
        print(f"\033[92m{message}\033[00m")

    @staticmethod
    def log_blue(message):
        """Logs a message to console in blue color.""" ""
        print(f"\033[94m{message}\033[00m")
