import random


class BasicMazeOperations:
    """Holds operations common to all maze generation phases' algorithms."""

    def __init__(self, size):
        self.size = size

    def _get_all_neighbors(self, node: int) -> [int]:
        size = self.size
        neighbors = []
        (row, column) = self._get_row_and_column(node)
        if row > 0:
            neighbors.append(node - size)
        if row < size - 1:
            neighbors.append(node + size)
        if column > 0:
            neighbors.append(node - 1)
        if column < size - 1:
            neighbors.append(node + 1)
        return neighbors

    def _get_row_and_column(self, node: int) -> (int, int):
        row = int(node / self.size)
        column = node % self.size
        return (row, column)

    def _pick_neighbor_in_random(self, neighbors):
        return neighbors[random.randint(0, len(neighbors) - 1)]
