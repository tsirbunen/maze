class UIHandlerToolkit:
    def __init__(
        self,
        listen_to_keystrokes,
        instructions,
        add_keystroke_action,
        perform_activity,
        event_processor,
        move_on_to_next_step,
        quit_program,
        update_screen,
        maze_size,
        on_timer,
        maze,
    ):
        self.listen_to_keystrokes = listen_to_keystrokes
        self.instructions = instructions
        self.add_keystroke_action = add_keystroke_action
        self.perform_activity = perform_activity
        self.event_processor = event_processor
        self.move_on_to_next_step = move_on_to_next_step
        self.quit_program = quit_program
        self.update_screen = update_screen
        self.maze_size = maze_size
        self.on_timer = on_timer
        self.maze = maze
