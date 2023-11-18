from src.graphical_ui.maze_activity import MazeActivity
from src.graphical_ui.ui_handler_toolkit import UIHandlerToolkit

VIEW_SOLVE_MAZE_OPTIONS = [
    "SOLVING THE MAZE",
    "Would you like to view solving the maze with different algorithms?",
    "- press 'E' to see DEAD END FILLER algorithm live",
    "- press 'W' to see WALL FOLLOWER algorithm live",
    "- press 'D' to see DIJKSTRA algorithm live",
    "- press 'A' to see A-STAR algorithm live",
    "- press 'H' for higher (2 X) speed",
    "- press 'L' for lower (1/2 X) speed",
    "- press 'Q' to quit the program",
]


class MazeSolvingStepHandler:
    def __init__(self, toolkit: UIHandlerToolkit):
        self.listen_to_keystrokes = toolkit.listen_to_keystrokes
        self._perform_activity = toolkit.perform_activity
        self.instructions = toolkit.instructions
        self.event_processor = toolkit.event_processor
        self.add_keystroke_action = toolkit.add_keystroke_action
        self.move_on_to_next_step = toolkit.move_on_to_next_step
        self.quit_program = toolkit.quit_program

    def handle(self):
        self.instructions.display_content(VIEW_SOLVE_MAZE_OPTIONS)
        self.add_keystroke_action(self._solve_maze_wall_follower, "w")
        self.add_keystroke_action(self.quit_program, "q")
        self.add_keystroke_action(self.event_processor.higher_speed, "h")
        self.add_keystroke_action(self.event_processor.lower_speed, "l")
        self.listen_to_keystrokes()

    def _solve_maze_wall_follower(self):
        self.event_processor.process()
        self._perform_activity(MazeActivity.SOLVE_WALL_FOLLOWER, True)
        self.instructions.clear_all_instructions()
        self.move_on_to_next_step()
