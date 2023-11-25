import math
import time

from src.events.event import AlgorithmEvent, EventType


class DeadEndFiller:
    """
    A class implementing the Dead End Filler algorithm for maze solving.
    Iterates over all nodes in a maze graph and removes those connections that are
    dead ends. If a node has only one connection and the node is not the start or
    the end node, then it is a dead end (and connection to it and from it
    is removed). In the end, all that is left in the original graph are the
    nodes in the path from start node to the end node.
    """

    def __init__(self, maze: [[int]], dispatch_event):
        self.maze = maze
        self.size = int(math.sqrt(len(maze)))
        self._dispatch_event = dispatch_event

    def solve(self) -> None:
        """Performs solving the maze using the Dead End Filler algorithm."""
        for node in range(0, self.size * self.size):
            self._proceed_alley_backward(node)
        self._dispatch_path()
        self._dispatch_event(AlgorithmEvent(EventType.SOLVING_COMPLETED, None))

    def _proceed_alley_backward(self, node):
        if self._is_dead_end_node(node):
            self._dispatch_filled_node(node)
            neighbor = self.maze[node][0]
            self._remove_dead_end_node_connections(node)
            self._proceed_alley_backward(neighbor)

    def _dispatch_filled_node(self, node) -> None:
        self._dispatch_event(AlgorithmEvent(EventType.PERMANENT_NODE, [node]))

    def _is_dead_end_node(self, node) -> bool:
        is_not_start_node = node != 0
        is_not_goal_node = node != self.size * self.size - 1
        is_alley_end = len(self.maze[node]) == 1
        return is_not_start_node and is_not_goal_node and is_alley_end

    def _remove_dead_end_node_connections(self, node) -> None:
        neighbor = self.maze[node][0]
        if node in self.maze[neighbor]:
            self.maze[neighbor].remove(node)
        self.maze[node] = []

    def _dispatch_path(self):
        path = self._extract_path()
        for node in path:
            self._dispatch_event(AlgorithmEvent(EventType.PATH_NODE, [node]))
            time.sleep(0.001)
        time.sleep(1)

    def _extract_path(self):
        """
        Forms the path from the nodes that still remain in the graph after all
        dead ends have been removed.
        """
        goal_node = self.size * self.size - 1
        current_node = 0
        path = []
        while True:
            path.append(current_node)
            if current_node == goal_node:
                break
            neighbors = self.maze[current_node]
            if len(neighbors) == 1:
                current_node = neighbors[0]
                continue
            previous = path[-2]
            current_node = neighbors[0] if neighbors[0] != previous else neighbors[1]
        return path
