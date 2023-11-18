from dataclasses import dataclass
import math
from enum import Enum

from src.events.event import AlgorithmEvent, EventType


class Side(Enum):
    """
    An enum telling the side of where the node is facing or where to turn.
    """

    LEFT = 1
    UP = 2
    RIGHT = 3
    DOWN = 4


@dataclass
class Turns:
    """
    A class holding data on what's on the left and on what's on the right hand side.
    """

    left: Side
    right: Side


TURNS = {
    Side.RIGHT: Turns(Side.UP, Side.DOWN),
    Side.UP: Turns(Side.LEFT, Side.RIGHT),
    Side.LEFT: Turns(Side.DOWN, Side.UP),
    Side.DOWN: Turns(Side.RIGHT, Side.LEFT),
}

ROW_AND_COLUMN_CHANGE_TO_GO_FORWARD = {
    Side.RIGHT: (0, 1),
    Side.UP: (-1, 0),
    Side.LEFT: (0, -1),
    Side.DOWN: (1, 0),
}


class WallFollower:
    """
    A class implementing the Wall Following algorithm for maze solving.
    Solves a maze by implementing an algorithm where the following is repeated:
    if there is an opening on the right, turn right, else if there is an opening
    in front, go forward, else if there is an opening on the left, turn left, else turn around.
    The wall follower might visit some nodes several times.
    """

    def __init__(self, maze: [[int]], dispatch_event):
        self.maze = maze
        self.size = int(math.sqrt(len(maze)))
        self._dispatch_event = dispatch_event
        self.current_node = self.row = self.column = 0
        self.facing = Side.RIGHT

    def solve(self):
        """Performs solving the maze using the wall follower algorithm."""
        self._dispatch_current_node()
        goal_node = self.size * self.size - 1
        while self.current_node != goal_node:
            for turn in self._get_turns_to_make():
                turn()
                if self._can_go_forward():
                    self._go_forward()
                    self._dispatch_current_node()
                    break

    def _dispatch_current_node(self):
        self._dispatch_event(
            AlgorithmEvent(EventType.PERMANENT_NODE, [self.current_node])
        )

    def _get_turns_to_make(self):
        return [
            self._turn_right,
            self._turn_left,
            self._turn_left,
            self._turn_left,
        ]

    def _turn_right(self):
        self.facing = TURNS[self.facing].right

    def _turn_left(self):
        self.facing = TURNS[self.facing].left

    def _can_go_forward(self):
        node_in_front = self._get_node_in_front()
        return node_in_front in self.maze[self.current_node]

    def _get_node_in_front(self):
        (row_change, column_change) = self._changes_if_going_forward()
        return self.current_node + row_change * self.size + column_change

    def _go_forward(self):
        (row_change, column_change) = self._changes_if_going_forward()
        self.row = self.row + row_change
        self.column = self.column + column_change
        self.current_node = self.current_node + row_change * self.size + column_change

    def _changes_if_going_forward(self):
        return ROW_AND_COLUMN_CHANGE_TO_GO_FORWARD[self.facing]
