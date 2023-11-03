import random
from heapq import heappush, heappop
from src.maze_generation.basic_maze_operations import BasicMazeOperations
from src.events.event import  EventType, MergeEvent



class Merger(BasicMazeOperations):
    def __init__(self, parameters, dispatch_event, twisted_variables: ([int], [[int]],[[int]])):
        super().__init__(parameters.size)
        self.waiting_labels = []
        self.focus_group_label = -1
        self.focus_group_nodes = [] 
        self.multiple_groups_remain = True
        self.dispatch_event = dispatch_event
        self.node_labels: [int] = twisted_variables[0]
        self.node_groups: [[int]] = twisted_variables[1]
        self.connections: [[int]] = twisted_variables[2]


    def perform(self):
        self.__arrange_group_labels_into_random_order()
        while self.multiple_groups_remain:
            self.__set_next_focus_group_label()
            self.__arrange_nodes_of_focus_group_into_random_order()
            self.__connect_one_focus_group_node_to_node_in_other_group_if_possible()


    def __arrange_group_labels_into_random_order(self):
        for label in range(0, len(self.node_groups)):
            random_location = random.randint(0, len(self.node_groups) - 1)
            heappush(self.waiting_labels, (random_location, label))
    
    def __set_next_focus_group_label(self):
        self.focus_group_label = heappop(self.waiting_labels)[1]

    def __arrange_nodes_of_focus_group_into_random_order(self):
        self.focus_group_nodes = []
        group_nodes = self.node_groups[self.focus_group_label]
        for i in range(0, len(group_nodes)):
            heappush(self.focus_group_nodes, (random.randint(0, len(group_nodes)), group_nodes[i]))
    
    def __connect_one_focus_group_node_to_node_in_other_group_if_possible(self):
        while len(self.focus_group_nodes) > 0:
            self.focus_node = heappop(self.focus_group_nodes)[1]
            self.dispatch_event(MergeEvent(self.focus_node, None, EventType.MERGE_FOCUS))
            neighbor_nodes = self.__get_unconnected_neighbors(self.focus_node)
            if len(neighbor_nodes) > 0:
                self.__connect_neighbor_group_to_focus_group(neighbor_nodes)
                break
    
    def __get_unconnected_neighbors(self, node):
        unconnected_neighbors = []
        for neighbor in self._get_all_neighbors(node):
            if self.node_labels[node] != self.node_labels[neighbor]:
                unconnected_neighbors.append(neighbor)
        return unconnected_neighbors

    def __connect_neighbor_group_to_focus_group(self, neighbor_nodes):
        neighbor_node = self._pick_neighbor_in_random(neighbor_nodes)
        self.__create_connections_between_nodes((self.focus_node, neighbor_node))
        current_group_label = self.node_labels[self.focus_node]
        neighbor_group_label = self.node_labels[neighbor_node]
        self.__relabel_nodes_of_smaller_group(current_group_label, neighbor_group_label)
        self.__check_if_multiple_groups_remain_after_combining([current_group_label, neighbor_group_label])
        heappush(self.waiting_labels, (len(self.node_groups[current_group_label]), current_group_label))

    def __create_connections_between_nodes(self, nodes):
        self.connections[nodes[0]].append(nodes[1])
        self.connections[nodes[1]].append(nodes[0])
        self.dispatch_event(MergeEvent(nodes[0], nodes[1], EventType.MERGE_CONNECT))

    def __relabel_nodes_of_smaller_group(self, current_label, neighbor_label):
        (new_label, label_to_relabel) = self.__get_smaller_group_to_relabel(current_label, neighbor_label)
        for node in self.node_groups[label_to_relabel]:
            self.node_labels[node] = new_label
            self.node_groups[new_label].append(node)
            self.dispatch_event(MergeEvent(node, None, EventType.MERGE_RELABEL))

    def __get_smaller_group_to_relabel(self, current_label, neighbor_label):
        should_relabel_neighbor = len(self.node_groups[neighbor_label]) < len(self.node_groups[current_label])
        label_to_relabel = neighbor_label if should_relabel_neighbor else current_label
        new_label = current_label if should_relabel_neighbor else neighbor_label
        return (new_label, label_to_relabel)

    def __check_if_multiple_groups_remain_after_combining(self, labels):
        target_size = self.size * self.size
        for label in labels:
            if len(self.node_groups[label]) == target_size:
                self.multiple_groups_remain = False


    def get_result(self) ->  [[int]]:
        return self.connections