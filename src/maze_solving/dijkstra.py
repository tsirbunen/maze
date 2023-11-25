import math
from heapq import heappush, heappop
import time

from src.events.event import AlgorithmEvent, EventType


class Dijkstra:
    """A class implementing the Dijksta algorithm for maze solving."""

    def __init__(self, maze: [[int]], dispatch_event):
        self.maze = maze
        self.size = int(math.sqrt(len(maze)))
        count = len(self.maze)
        self._dispatch_event = dispatch_event
        self._parents = [None] * (self.size * self.size)
        self._distances = [math.inf for _ in range(0, count)]
        self._node_heap = []
        self._handled = [False for _ in range(0, count)]

    def solve(self) -> None:
        """Performs solving the maze using the Dijksta algorithm."""
        start_node = 0
        self._distances[start_node] = 0
        heappush(self._node_heap, (0, start_node))
        while self._nodes_remain_to_be_handled():
            (distance, index) = heappop(self._node_heap)
            self._dispatch_current_node(index)
            if self._handled[index]:
                continue
            self._handled[index] = True
            self._update_neighbors(index, distance)
        self._dispatch_path()
        self._dispatch_event(AlgorithmEvent(EventType.SOLVING_COMPLETED, None))

    def _nodes_remain_to_be_handled(self):
        return len(self._node_heap) > 0

    def _update_neighbors(self, index, distance):
        for neighbor_index in self.maze[index]:
            self._dispatch_neighbor_node(neighbor_index)
            current_distance = self._distances[neighbor_index]
            new_distance = distance + 1
            self._update_distance_if_smaller(
                index, new_distance, current_distance, neighbor_index
            )

    def _update_distance_if_smaller(
        self, index, new_distance, current_distance, neighbor_index
    ):
        if new_distance < current_distance:
            self._distances[neighbor_index] = new_distance
            self._parents[neighbor_index] = index
            heappush(self._node_heap, (new_distance, neighbor_index))

    def _dispatch_current_node(self, node):
        self._dispatch_event(AlgorithmEvent(EventType.PERMANENT_NODE, [node]))

    def _dispatch_neighbor_node(self, node):
        self._dispatch_event(AlgorithmEvent(EventType.BLINK_NODE, [node]))

    def _dispatch_path(self):
        path = self._extract_path()
        for node in path:
            self._dispatch_event(AlgorithmEvent(EventType.PATH_NODE, [node]))
            time.sleep(0.001)
        time.sleep(1)

    def _extract_path(self):
        end_node = self.size * self.size - 1
        path = [end_node]
        path_index = end_node
        while True:
            parent = self._parents[path_index]
            path.append(parent)
            if parent == 0:
                break
            path_index = parent
        path.reverse()
        return path
