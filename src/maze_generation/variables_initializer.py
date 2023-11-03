import random

from src.maze_parameters.maze_type import MazeType
from src.maze_parameters.maze_parameters import MazeParameters



class VariablesInitializer:
    def __init__(self, size: int):
        self.size = size
        self.unlabeled_nodes = []
        self.labeling_statuses = []
        self.node_labels = []
        self.node_groups = []
        self.connections = []
        for i in range(0, self.size * self.size):
            self.unlabeled_nodes.append(i)
            self.labeling_statuses.append(False)
            self.node_labels.append(-1)
            self.connections.append([])
        random.shuffle(self.unlabeled_nodes)

    def get_result(self):
        return (self.unlabeled_nodes, self.labeling_statuses, self.node_labels, self.node_groups, self.connections)
    