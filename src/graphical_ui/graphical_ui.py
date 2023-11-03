from .screen import ScreenProvider


class GraphicalUI:
    def __init__(self, maze_connections: [[int]]) -> None:

        self.screen_provider = ScreenProvider()


        self.screen_provider.set_exit_on_click()

