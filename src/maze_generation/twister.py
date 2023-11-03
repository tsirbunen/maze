from src.events.event import TwistEvent, EventType
from src.maze_generation.basic_maze_operations import BasicMazeOperations



class Twister(BasicMazeOperations):
    def __init__(self, parameters, dispatch_event, variables: ([int], [bool], [int], [[int]], [[int]])):
        super().__init__(parameters.size)
        self.dispatch_event = dispatch_event
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
        while self.nodes_remain_to_be_labeled():
            self.node = self.unlabeled_nodes[self.index]
            if self.node_has_not_been_labeled_yet(self.node):
                self.label_node(self.node, is_new_group=True)
                self.dispatch_event(TwistEvent(self.node, None))
                self.perform_one_random_walk_from_node()
                self.label += 1
            self.index += 1


    def nodes_remain_to_be_labeled(self) -> bool:
        return self.index < len(self.unlabeled_nodes)
    

    def node_has_not_been_labeled_yet(self, node) -> bool:
        return not self.labeling_statuses[node]

    def perform_one_random_walk_from_node(self) -> None:
        while True:
            neighbor = self.find_acceptable_neighbor_in_random()
            if neighbor is None:
                break
            self.label_node(neighbor)
            self.add_connections(self.node, neighbor)
            self.dispatch_event(TwistEvent(neighbor, self.node))
            self.previous_node = self.node
            self.node = neighbor
    
    def find_acceptable_neighbor_in_random(self) -> int:
        neighbors = self._get_all_neighbors(self.node)
        if len(neighbors) > 0:
            neighbor = self._pick_neighbor_in_random(neighbors)
            if self.neighbor_is_acceptable(neighbor, self.node, self.previous_node):
                return neighbor
        return None
        

    def label_node(self, node, is_new_group = False)-> None:
        self.labeling_statuses[node] = True
        if is_new_group:
            self.previous_node = -1
            self.node_groups.append([])
        self.node_groups[self.label].append(node)
        self.node_labels[node] = self.label
    
    def add_connections(self, node, neighbor)-> None:
        self.connections[node].append(neighbor)
        self.connections[neighbor].append(node)

    def neighbor_is_acceptable(self, neighbor, current_node, previous_node) -> bool:
        is_labeled = self.node_labels[neighbor] != -1
        if is_labeled:
            return False
        forms_a_corridor = self.nodes_form_a_long_corridor([previous_node, current_node, neighbor])
        if forms_a_corridor:
            return False
        return True

    def nodes_form_a_long_corridor(self, nodes: [int]) -> bool:
        rows = []
        columns = []
        for node in nodes:
            (row, column) = self._get_row_and_column(node)
            rows.append(row)
            columns.append(column)
        return len(set(rows)) == 1 or len(set(columns)) == 1

    
    def get_result(self) -> ([int], [[int]],[[int]]):
        return (self.node_labels, self.node_groups, self.connections)
        

