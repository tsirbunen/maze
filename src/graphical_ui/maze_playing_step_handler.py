import enum


from src.graphical_ui.player import Player
from src.graphical_ui.point import Point
from src.graphical_ui.stamp import Stamp
from src.graphical_ui.ui_handler_toolkit import UIHandlerToolkit

PLAY_MAZE_OPTIONS = [
    "PLAYING THE MAZE",
    "Would you like to try playing?",
    "- press 'Y' to play the maze",
    "- press 'N' to skip playing",
    "- press 'Q' to quit the program",
]

PLAY_MAZE_CONTENT = [
    "PLAYING THE MAZE",
    "- use arrows to move around the maze",
    "- press 'S' to stop playing",
    "- press 'V' to view solving maze",
    "- press 'Q' to quit the program",
]


class MazePlayingStepHandler:
    def __init__(self, toolkit: UIHandlerToolkit):
        self.listen_to_keystrokes = toolkit.listen_to_keystrokes
        self._perform_activity = toolkit.perform_activity
        self.instructions = toolkit.instructions
        # self.event_processor = toolkit.event_processor
        self.add_keystroke_action = toolkit.add_keystroke_action
        self.move_on_to_next_step = toolkit.move_on_to_next_step
        self.quit_program = toolkit.quit_program
        self.maze_size = toolkit.maze_size
        self.update_screen = toolkit.update_screen
        self.on_timer = toolkit.on_timer
        self.maze = toolkit.maze
        self.player = None

    def handle(self):
        self.instructions.clear_all_instructions()
        self.instructions.display_content(PLAY_MAZE_OPTIONS)
        self.add_keystroke_action(self._play, "y")
        self.add_keystroke_action(self._skip_playing, "n")
        self.add_keystroke_action(self.quit_program, "q")
        self.listen_to_keystrokes()

    def _skip_playing(self):
        self.instructions.clear_all_instructions()
        self.move_on_to_next_step()

    def _move_on_to_view_solving_maze(self):
        self.player.stop_playing()
        self.instructions.clear_all_instructions()
        self.move_on_to_next_step()

    def _play(self):
        self.player = Player(
            self.maze_size, self.update_screen, self.on_timer, self.maze
        )
        self.player.setup_goal()
        self.player.setup_player()
        # self.update_screen()
        self.add_keystroke_action(self.player.go_up, "Up")
        self.add_keystroke_action(self.player.go_down, "Down")
        self.add_keystroke_action(self.player.go_left, "Left")
        self.add_keystroke_action(self.player.go_right, "Right")
        self.add_keystroke_action(self.player.stop_playing, "s")
        self.add_keystroke_action(self._move_on_to_view_solving_maze, "v")
        self.add_keystroke_action(self.quit_program, "q")
        self.listen_to_keystrokes()
        # self.event_processor.process()
        # self._perform_activity(MazeActivity.GENERATE, True)
        self.instructions.clear_all_instructions()
        self.instructions.display_content(PLAY_MAZE_CONTENT)

    # def _generate_maze_without_live_viewing(self):
    #     self._perform_activity(MazeActivity.GENERATE, False)
