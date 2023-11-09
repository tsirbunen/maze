from src.events.event import AlgorithmEvent, EventType
from .basic_maze_operations import BasicMazeOperations


class Twister(BasicMazeOperations):
    def __init__(
        self,
        parameters,
        dispatch_event,
        variables: ([int], [bool], [int], [[int]], [[int]]),
    ):
        super().__init__(parameters.size)
        self._dispatch_event = dispatch_event
        self.node = None
        self.label = 0
        self.previous_node = -1
        self.index = 0
        self.unlabeled_nodes: [int] = variables[0]
        self.labeling_statuses: [bool] = variables[1]
        self.node_labels: [int] = variables[2]
        self.node_groups: [[int]] = variables[3]
        self.connections: [[int]] = variables[4]

    def perform(self) -> None:
        while self._nodes_remain_to_be_labeled():
            self.node = self.unlabeled_nodes[self.index]
            if self._node_has_not_been_labeled_yet(self.node):
                self._label_node(self.node, is_new_group=True)
                self._dispatch_event(
                    AlgorithmEvent(EventType.PERMANENT_NODE, [self.node])
                )
                self._perform_one_random_walk_from_node()
                self.label += 1
            self.index += 1
        self._dispatch_event(AlgorithmEvent(EventType.PHASE_COMPLETED, []))

    def _nodes_remain_to_be_labeled(self) -> bool:
        return self.index < len(self.unlabeled_nodes)

    def _node_has_not_been_labeled_yet(self, node) -> bool:
        return not self.labeling_statuses[node]

    def _perform_one_random_walk_from_node(self) -> None:
        while True:
            neighbor = self._find_acceptable_neighbor_in_random()
            if neighbor is None:
                break
            self._label_node(neighbor)
            self._add_connections(self.node, neighbor)
            self._dispatch_event(AlgorithmEvent(EventType.PERMANENT_NODE, [neighbor]))
            self._dispatch_event(
                AlgorithmEvent(EventType.REMOVE_WALL, [self.node, neighbor])
            )
            self.previous_node = self.node
            self.node = neighbor

    def _find_acceptable_neighbor_in_random(self) -> int:
        neighbors = self._get_all_neighbors(self.node)
        if len(neighbors) > 0:
            neighbor = self._pick_neighbor_in_random(neighbors)
            if self._neighbor_is_acceptable(neighbor, self.node, self.previous_node):
                return neighbor
        return None

    def _label_node(self, node, is_new_group=False) -> None:
        self.labeling_statuses[node] = True
        if is_new_group:
            self.previous_node = -1
            self.node_groups.append([])
        self.node_groups[self.label].append(node)
        self.node_labels[node] = self.label

    def _add_connections(self, node, neighbor) -> None:
        self.connections[node].append(neighbor)
        self.connections[neighbor].append(node)

    def _neighbor_is_acceptable(self, neighbor, current_node, previous_node) -> bool:
        is_labeled = self.node_labels[neighbor] != -1
        if is_labeled:
            return False
        forms_a_corridor = self._nodes_form_a_long_corridor(
            [previous_node, current_node, neighbor]
        )
        if forms_a_corridor:
            return False
        return True

    def _nodes_form_a_long_corridor(self, nodes: [int]) -> bool:
        rows = []
        columns = []
        for node in nodes:
            (row, column) = self._get_row_and_column(node)
            rows.append(row)
            columns.append(column)
        return len(set(rows)) == 1 or len(set(columns)) == 1

    def get_result(self) -> ([int], [[int]], [[int]]):
        return (self.node_labels, self.node_groups, self.connections)
