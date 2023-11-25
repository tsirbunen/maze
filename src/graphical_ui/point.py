from dataclasses import dataclass


@dataclass
class Point:
    """Describes the location on the screen."""

    x: int
    y: int
