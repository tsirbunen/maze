import time
from .wall import Wall
from .wall_position import WallPosition
from .constants import ELEMENT_SIZE
from .point import Point


class MazeWalls:
    """Handles all wall-related actions (drawing, storing and removing maze walls between nodes)."""

    def __init__(self, origo: Point, maze_size: int, update_screen):
        self.maze_origo = origo
        self.maze_size = maze_size
        self._update_screen = update_screen
        self.walls_of_all_nodes = []

    def draw_walls_between_nodes(self):
        """Creates a wall to the right and below of each node where ever possible."""
        for row in range(0, self.maze_size):
            for column in range(0, self.maze_size):
                node_walls = self._create_walls_for_one_node(row, column)
                self.walls_of_all_nodes.append(node_walls)
        self._update_screen()

    def _create_walls_for_one_node(self, row, column):
        (x, y) = self._get_node_origo(row, column)
        wall_on_right = self._create_wall_on_right(column, x, y)
        wall_below = self._create_wall_below(row, x, y)
        return {
            WallPosition.RIGHT: wall_on_right,
            WallPosition.BELOW: wall_below,
        }

    def _get_node_origo(self, row, column):
        x = self.maze_origo.x + (column + 1) * ELEMENT_SIZE
        y = self.maze_origo.y - row * ELEMENT_SIZE
        return (x, y)

    def _create_wall_on_right(self, column, x, y) -> Wall | None:
        if column < self.maze_size - 1:
            return Wall(Point(x, y), 90)
        return None

    def _create_wall_below(self, row, x, y) -> Wall | None:
        if row < self.maze_size - 1:
            return Wall(Point(x, y - ELEMENT_SIZE), 180)
        return None

    def remove_wall_between_nodes_with_a_blink(self, nodes):
        """Deletes a wall between two maze nodes on screen permanently with a blink effect."""
        [node, neighbor] = self._arrange_nodes_asc(nodes)
        position = self._get_position_on_node_of_wall_to_remove(node, neighbor)
        wall_to_remove = self._get_wall_to_remove(node, position)
        self._blink_wall(wall_to_remove)
        self._update_walls_of_all_nodes(node, position)
        self._clear_wall_from_screen(wall_to_remove)
        self._update_screen()

    def _arrange_nodes_asc(self, nodes):
        nodes.sort()
        return nodes

    def _get_wall_to_remove(self, node, node_wall_position):
        return self.walls_of_all_nodes[node][node_wall_position]

    def _get_position_on_node_of_wall_to_remove(self, node, neighbor):
        if node + 1 == neighbor:
            return WallPosition.RIGHT
        if node + self.maze_size == neighbor:
            return WallPosition.BELOW
        raise ValueError("No such wall exists")

    def _blink_wall(self, wall):
        if wall is None:
            return
        wall.draw_wall_in_blink_color()
        self._update_screen()
        time.sleep(0.5)

    def _update_walls_of_all_nodes(self, node, node_wall_position):
        self.walls_of_all_nodes[node][node_wall_position] = None

    def _clear_wall_from_screen(self, wall_to_remove):
        if wall_to_remove is None:
            return
        wall_to_remove.clear()
