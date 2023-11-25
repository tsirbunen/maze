class Toolkit:
    """Holds handles to control UI elements according to events and actions."""

    def __init__(
        self,
        show_instructions,
        perform_activity,
        event_processor,
        perform_next_step,
        update_screen,
        maze_size,
        on_timer,
        maze,
        add_on_keystroke_actions,
    ):
        self.show_instructions = show_instructions
        self.perform_activity = perform_activity
        self.event_processor = event_processor
        self.perform_next_step = perform_next_step
        self.update_screen = update_screen
        self.maze_size = maze_size
        self.on_timer = on_timer
        self.maze = maze
        self.add_on_keystroke_actions = add_on_keystroke_actions
