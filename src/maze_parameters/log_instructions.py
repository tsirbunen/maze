from src.utils.logger import Logger
from .constants import WELCOME, INSTRUCTIONS, YOUR_INPUT_TITLE

def log_instructions():
    for line in WELCOME:
        Logger.logPink(line)

    for line_group in INSTRUCTIONS:
        for line in range(len(line_group)):
            to_print = line_group[line]
            if line == 0:
                Logger.logPink(to_print)
            else:
                Logger.logYellow(to_print)
    
    Logger.logPink(YOUR_INPUT_TITLE)

