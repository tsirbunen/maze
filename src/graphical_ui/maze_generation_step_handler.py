import enum

from src.graphical_ui.maze_activity import MazeActivity
from src.graphical_ui.ui_handler_toolkit import UIHandlerToolkit

GENERATE_MAZE_OPTIONS = [
    "MAZE GENERATION",
    "Would you like to view maze generation steps live?",
    "- press 'G' to see live maze generation",
    "- press 'S' to skip live viewing",
    "- press 'Q' to quit the program",
]

GENERATE_MAZE_CONTENT = [
    "TWIST & MERGE GENERATION ALGORITHM",
    "- press 'H' for higher (2 X) speed",
    "- press 'L' for lower (1/2 X) speed",
    "- press 'S' to stop viewing maze generation",
    "- press 'Q' to quit the program",
]


class MazeGenerationStepHandler:
    def __init__(self, toolkit: UIHandlerToolkit):
        self.listen_to_keystrokes = toolkit.listen_to_keystrokes
        self._perform_activity = toolkit.perform_activity
        self.instructions = toolkit.instructions
        self.event_processor = toolkit.event_processor
        self.add_keystroke_action = toolkit.add_keystroke_action
        self.move_on_to_next_step = toolkit.move_on_to_next_step
        self.quit_program = toolkit.quit_program

    def handle(self):
        self.instructions.display_content(GENERATE_MAZE_OPTIONS)
        self.add_keystroke_action(self._generate_maze_with_live_viewing, "g")
        self.add_keystroke_action(self._generate_maze_without_live_viewing, "s")
        self.add_keystroke_action(self.quit_program, "q")
        self.listen_to_keystrokes()

    def _generate_maze_with_live_viewing(self):
        self.add_keystroke_action(self.event_processor.higher_speed, "h")
        self.add_keystroke_action(self.event_processor.lower_speed, "l")
        self.add_keystroke_action(self.event_processor.stop_processing, "s")
        self.add_keystroke_action(self.quit_program, "q")
        self.listen_to_keystrokes()
        self.event_processor.process()
        self._perform_activity(MazeActivity.GENERATE, True)
        self.instructions.clear_all_instructions()
        self.instructions.display_content(GENERATE_MAZE_CONTENT)

    def _generate_maze_without_live_viewing(self):
        self._perform_activity(MazeActivity.GENERATE, False)
        maze = self._perform_activity(MazeActivity.GET_MAZE, None)
        self._remove_walls_from_ready_maze(maze)

        # Tähän jotain odottelua, että on varmasti valmis
        self.instructions.clear_all_instructions()
        self.move_on_to_next_step()

    def _remove_walls_from_ready_maze(self, maze):
        for node, node_connections in enumerate(maze):
            print(f"Node {node} has connections {node_connections}")
            for connected_node in node_connections:
                print(f"Remove wall between {node} and {connected_node}")
                self.event_processor.remove_wall([node, connected_node])
