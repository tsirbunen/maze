import random


class VariablesInitializer:
    """Initializes the variables needed in the Twist & Merge maze generation algorithm."""

    def __init__(self, size: int):
        self.size = size
        self.unlabeled_nodes = []
        self.labeling_statuses = []
        self.node_labels = []
        self.node_groups = []
        self.connections = []

    def get_result(self):
        """Returns the initialized Maze generation variables."""
        for i in range(0, self.size * self.size):
            self.unlabeled_nodes.append(i)
            self.labeling_statuses.append(False)
            self.node_labels.append(-1)
            self.connections.append([])
        random.shuffle(self.unlabeled_nodes)
        return (
            self.unlabeled_nodes,
            self.labeling_statuses,
            self.node_labels,
            self.node_groups,
            self.connections,
        )
