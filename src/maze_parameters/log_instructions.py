from src.utils.logger import Logger
from .constants import WELCOME, INSTRUCTIONS, YOUR_INPUT_TITLE


def log_instructions():
    """Log use instructions to the console."""
    for line in WELCOME:
        Logger.log_pink(line)

    for line_group in INSTRUCTIONS:
        for index, line in enumerate(line_group):
            if index == 0:
                Logger.log_pink(line)
            else:
                Logger.log_yellow(line)

    Logger.log_pink(YOUR_INPUT_TITLE)
