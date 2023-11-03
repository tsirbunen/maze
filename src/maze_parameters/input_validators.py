from .constants import MIN_SIZE, MAX_SIZE


def validate_maze_size(value: str) -> bool:
    try:
        size = int(value)
        return MIN_SIZE <= size <= MAX_SIZE
    except ValueError:
        return False


def validate_maze_type(value: str) -> bool:
    return value == 's' or value == 'm'



