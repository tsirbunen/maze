import time

from src.events.event_queue import EventQueue
from src.graphical_ui.maze_activity import MazeActivity
from src.graphical_ui.maze_generation_step_handler import (
    MazeGenerationStepHandler,
)
from src.graphical_ui.events_processor import EventsProcessor
from src.graphical_ui.maze_playing_step_handler import MazePlayingStepHandler
from src.graphical_ui.maze_solving_step_handler import MazeSolvingStepHandler
from src.graphical_ui.player import Player
from src.graphical_ui.stamp import Stamp
from src.graphical_ui.stamp_mode import StampMode
from src.graphical_ui.ui_handler_toolkit import UIHandlerToolkit
from .user_instructions import UserInstructions


from .status_stamps import StatusStamps
from .maze_border import MazeBorder
from .maze_walls import MazeWalls
from .point import Point
from .constants import ELEMENT_SIZE
from .screen_provider import ScreenProvider


class GraphicalUI:
    """GraphicalUI is responsible for ORCHESTRATING all maze related things."""

    def __init__(self, maze_size: int, event_queue: EventQueue, perform_activity):
        self.maze = None
        self.maze_size = maze_size
        self._perform_activity = perform_activity
        self.screen_provider = ScreenProvider()
        self.update_screen = self.screen_provider.update
        self.origo = self._get_maze_origo(maze_size)
        self.walls = MazeWalls(self.origo, maze_size, self.update_screen)
        self.status_stamps = StatusStamps(self.origo, maze_size, self.update_screen)
        self._setup_border_walls_and_status_stamps(maze_size)
        self.instructions = UserInstructions()
        self.event_processor = EventsProcessor(
            event_queue, self.status_stamps, self.walls, self._move_on_to_next_step
        )
        self._steps = [self._generate_maze, self._play_maze, self._view_solving_maze]
        # self.step_handlers = [MazeGenerationStepHandler, MazePlayingStepHandler]
        self.toolkit = None
        self._build_toolkit()
        self._move_on_to_next_step()
        self.screen_provider.set_exit_on_click()

    def _build_toolkit(self):
        self.toolkit = UIHandlerToolkit(
            listen_to_keystrokes=self.screen_provider.listen_to_keystrokes,
            instructions=self.instructions,
            add_keystroke_action=self.screen_provider.add_keystroke_action,
            perform_activity=self._perform_activity,
            event_processor=self.event_processor,
            move_on_to_next_step=self._move_on_to_next_step,
            quit_program=self._quit_program,
            update_screen=self.update_screen,
            maze_size=self.maze_size,
            on_timer=self.screen_provider.on_timer,
            maze=self.maze,
        )

    def _move_on_to_next_step(self):
        if len(self._steps) > 0:
            step = self._steps.pop(0)
            step()

    def _generate_maze(self):
        handler = MazeGenerationStepHandler(self.toolkit)
        handler.handle()

    def _play_maze(self):
        self.maze = self._perform_activity(MazeActivity.GET_MAZE, None)
        self.toolkit.maze = self.maze
        handler = MazePlayingStepHandler(self.toolkit)
        handler.handle()

    def _view_solving_maze(self):
        handler = MazeSolvingStepHandler(self.toolkit)
        handler.handle()

    def _get_maze_origo(self, maze_size) -> Point:
        x = -(maze_size / 2) * ELEMENT_SIZE
        y = (maze_size / 2) * ELEMENT_SIZE
        return Point(x, y)

    def _setup_border_walls_and_status_stamps(self, maze_size):
        maze_border = MazeBorder(self.origo, maze_size, self.update_screen)
        maze_border.draw_maze_border_walls()
        self.walls.draw_walls_between_nodes()
        self.status_stamps.create_status_stamps()

    def set_maze(self, maze):
        self.maze = maze

    def _quit_program(self):
        self.screen_provider.quit_program()
