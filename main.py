from src.maze_parameters.parameters_querier import ParametersQuerier
from src.maze_parameters.log_instructions import log_instructions
from src.maze_generation.maze_generator import MazeGenerator
from src.graphical_ui.graphical_ui import GraphicalUI


log_instructions()
parameters = ParametersQuerier().get_parameters()

maze_generator = MazeGenerator(parameters)
maze_generator.generate()
maze_connection = maze_generator.get_finished_maze()

graphical_ui = GraphicalUI()