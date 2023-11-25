from src.events.event_queue import EventQueue
from src.graphical_ui.maze_elements_controller import MazeElementsController
from src.graphical_ui.maze_generation_handler import MazeGenerationHandler
from src.graphical_ui.events_processor import EventsProcessor
from src.graphical_ui.maze_playing_handler import MazePlayingHandler
from src.graphical_ui.maze_solving_handler import MazeSolvingHandler
from src.graphical_ui.toolkit import Toolkit


class GraphicalUI:
    """GraphicalUI is responsible for ORCHESTRATING all UI-related things."""

    def __init__(self, maze_size: int, event_queue: EventQueue, perform_activity):
        self.maze_elements_controller = MazeElementsController(maze_size)
        self.event_processor = EventsProcessor(
            event_queue,
            self.maze_elements_controller.handle_stamp_action,
            self.maze_elements_controller.remove_wall_between_nodes,
            self._perform_next_step,
        )
        self._step_handlers = [
            MazeGenerationHandler,
            MazePlayingHandler,
            MazeSolvingHandler,
        ]
        self.toolkit = None
        self._build_toolkit(maze_size, perform_activity)
        self.handler = None
        self._perform_next_step()
        self.maze_elements_controller.set_exit_on_click()

    def _build_toolkit(self, maze_size, perform_activity):
        self.toolkit = Toolkit(
            show_instructions=self.maze_elements_controller.show_instructions,
            perform_activity=perform_activity,
            event_processor=self.event_processor,
            perform_next_step=self._perform_next_step,
            update_screen=self.maze_elements_controller.update_screen,
            maze_size=maze_size,
            on_timer=self.maze_elements_controller.perform_after_delay,
            maze=None,
            add_on_keystroke_actions=self.maze_elements_controller.add_on_keystroke_actions,
        )

    def _perform_next_step(self, maze=None):
        if maze is not None:
            self.toolkit.maze = maze
        if len(self._step_handlers) > 0:
            self.handler = self._step_handlers.pop(0)
            self.handler = self.handler(self.toolkit)
        self.handler.handle()
