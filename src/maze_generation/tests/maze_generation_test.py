from src.events.event import EventType
from src.maze_generation.tests.helpers import dispatch_event
from src.maze_generation.maze_generator import MazeGenerator
from src.maze_generation.merger import Merger
from src.maze_generation.twister import Twister
from src.maze_generation.variables_initializer import VariablesInitializer
from src.maze_parameters.maze_parameters import MazeParameters
from src.maze_parameters.maze_type import MazeType
import src.maze_generation.tests.helpers as helpers


def test_maze_generation_variables_are_correctly_initialized_for_mazes_of_different_size():
    sizes = [3, 12, 37]
    for size in sizes:
        initializer = VariablesInitializer(size)
        (
            unlabeled_nodes,
            labeling_statuses,
            node_labels,
            node_groups,
            connections,
        ) = initializer.get_result()
        assert_unlabeled_nodes_are_appropriate(size, unlabeled_nodes)
        assert_labeling_statuses_are_appropriate(size, labeling_statuses)
        assert_node_labels_are_appropriate(size, node_labels)
        assert_node_groups_are_appropriate(node_groups)
        assert_connections_are_appropriate(size, connections)


def assert_unlabeled_nodes_are_appropriate(size, unlabeled_nodes):
    assert len(unlabeled_nodes) == size * size
    for i in range(0, size * size):
        assert i in unlabeled_nodes


def assert_labeling_statuses_are_appropriate(size, labeling_statuses):
    assert len(labeling_statuses) == size * size
    for i in range(0, size * size):
        assert not labeling_statuses[i]


def assert_node_labels_are_appropriate(size, node_labels):
    assert len(node_labels) == size * size
    for i in range(0, size * size):
        assert node_labels[i] == -1


def assert_node_groups_are_appropriate(node_groups):
    assert len(node_groups) == 0


def assert_connections_are_appropriate(size, connections):
    assert len(connections) == size * size
    for i in range(0, size * size):
        assert len(connections[i]) == 0


def test_neighbor_cells_are_correctly_identified():
    test_input_expected_output_data = [
        (4, 3, [2, 7]),
        (4, 7, [3, 6, 11]),
        (4, 12, [8, 13]),
        (4, 4, [0, 5, 8]),
        (4, 10, [6, 9, 11, 14]),
        (5, 24, [19, 23]),
        (5, 23, [18, 22, 24]),
    ]
    for size, node, expected_neighbors in test_input_expected_output_data:
        initializer = VariablesInitializer(size)
        twister = Twister(
            MazeParameters(size, MazeType.SINGLE),
            dispatch_event,
            initializer.get_result(),
        )
        neighbors = twister._get_all_neighbors(node)
        assert len(neighbors) == len(expected_neighbors)
        for n in neighbors:
            assert n in expected_neighbors


def test_nodes_form_a_corridor():
    test_input_expected_output_data = [
        (4, [1, 2, 3], True),
        (4, [1, 2, 6], False),
        (5, [17, 18, 19], True),
        (5, [17, 18, 23], False),
    ]
    for size, nodes, expected_result in test_input_expected_output_data:
        initializer = VariablesInitializer(size)
        twister = Twister(
            MazeParameters(size, MazeType.SINGLE),
            dispatch_event,
            initializer.get_result(),
        )
        result = twister._nodes_form_a_long_corridor(nodes)
        assert result == expected_result


def test_twisting_produces_proper_variable_values():
    test_input_data = [4, 5, 6, 17]
    for size in test_input_data:
        initializer = VariablesInitializer(size)
        twister = Twister(
            MazeParameters(size, MazeType.SINGLE),
            dispatch_event,
            initializer.get_result(),
        )
        twister.perform()
        (node_labels, node_groups, all_connections) = twister.get_result()
        assert_not_too_many_connections_per_node(all_connections)
        assert_connections_exist_in_both_directions(all_connections)
        assert_node_labels_have_been_assigned_max_allowed_values(
            node_groups, node_labels
        )
        assert_all_nodes_are_in_a_group_and_only_in_one_group(node_groups, size)
        assert_node_groups_match_connections_data(node_groups, all_connections)
        assert_node_labels_match_node_group_data(node_groups, node_labels)


def test_twisting_publishes_expected_events(mocker):
    test_input_data = [5, 9]
    for size in test_input_data:
        spy = mocker.spy(helpers, "dispatch_event")
        initializer = VariablesInitializer(size)
        twister = Twister(
            MazeParameters(size, MazeType.SINGLE),
            helpers.dispatch_event,
            initializer.get_result(),
        )
        twister.perform()
        permanent_node_events = size * size
        phase_completed_event = 1
        assert spy.call_count >= permanent_node_events + phase_completed_event
        nodes = []
        for call in spy.call_args_list:
            event = call[0][0]
            if event.algorithm_event_type == EventType.PERMANENT_NODE:
                nodes.append(event.nodes[0])
        assert len(set(nodes)) == (size * size)


def assert_not_too_many_connections_per_node(all_connections):
    for connections in all_connections:
        assert len(connections) <= 2


def assert_connections_exist_in_both_directions(all_connections):
    for node_index, node_connections in enumerate(all_connections):
        node_connections = all_connections[node_index]
        for neighbor in node_connections:
            assert node_index in all_connections[neighbor]


def assert_node_labels_have_been_assigned_max_allowed_values(node_groups, node_labels):
    max_label = len(node_groups) - 1
    for label in node_labels:
        assert label != -1
        assert label <= max_label


def assert_all_nodes_are_in_a_group_and_only_in_one_group(node_groups, size):
    all_nodes = []
    for group in node_groups:
        all_nodes += group
    for index in range(0, size * size):
        assert index in all_nodes
        assert len(all_nodes) == size * size


def assert_node_groups_match_connections_data(node_groups, all_connections):
    for group in node_groups:
        if len(group) == 1:
            assert len(all_connections[group[0]]) == 0
        else:
            connections_with_one = []
            for index, connection in enumerate(group):
                if len(all_connections[connection]) == 1:
                    connections_with_one.append(index)
            assert len(connections_with_one) == 2


def assert_node_labels_match_node_group_data(node_groups, node_labels):
    for label, node_group in enumerate(node_groups):
        label_indexes_in_node_labels = [
            i for i in range(len(node_labels)) if node_labels[i] == label
        ]
        assert len(label_indexes_in_node_labels) == len(node_group)


def test_merging_produces_a_valid_maze():
    size = 3
    node_labels = [2, 5, 1, 3, 4, 6, 3, 7, 0]
    node_groups = [[8], [2], [0], [6, 3], [4], [1], [5], [7]]
    all_connections = [[], [], [], [6], [], [], [3], [], []]
    twisted_variables = (node_labels, node_groups, all_connections)
    merger = Merger(
        MazeParameters(size, MazeType.SINGLE), dispatch_event, twisted_variables
    )
    merger.perform()
    connections = merger.get_result()
    assert_generated_maze_has_correct_dimensions(size, connections)
    assert_every_node_in_generated_maze_is_connected_to_other_nodes(connections)
    assert_generated_maze_contains_no_loops_and_all_nodes_are_connected(
        size, connections
    )


def test_maze_generator_produces_valid_single_solution_mazes():
    test_sizes = [4, 7, 13, 22, 46]
    for size in test_sizes:
        maze_generator = MazeGenerator(MazeParameters(size, MazeType.SINGLE))
        # Note: Replace the dispatch function in this test with a dummy because
        # the real function waits in between events for a little while and that
        # would cause the tests to run too slowly.
        maze_generator.dispatch_event = helpers.dispatch_event
        maze_generator.generate(True)
        connections = maze_generator.get_finished_maze()
        assert_generated_maze_has_correct_dimensions(size, connections)
        assert_every_node_in_generated_maze_is_connected_to_other_nodes(connections)
        assert_generated_maze_contains_no_loops_and_all_nodes_are_connected(
            size, connections
        )


def assert_generated_maze_has_correct_dimensions(size, connections):
    assert size * size == len(connections)


def assert_every_node_in_generated_maze_is_connected_to_other_nodes(connections):
    for node_connections in connections:
        assert 0 < len(node_connections) < 5


def assert_generated_maze_contains_no_loops_and_all_nodes_are_connected(
    size, connections
):
    visited_statuses = [False for _ in range(0, size * size)]
    assert visit_all_children_only_once(0, -1, visited_statuses, connections)
    assert_nodes_of_generated_maze_form_one_connected_group(size, visited_statuses)


def visit_all_children_only_once(node, parent, visited_statuses, connections):
    if visited_statuses[node]:
        return False
    visited_statuses[node] = True
    children = connections[node]
    for child in children:
        if child != parent:
            visit_once = visit_all_children_only_once(
                child, node, visited_statuses, connections
            )
            if not visit_once:
                return False
    return True


def assert_nodes_of_generated_maze_form_one_connected_group(size, visited_statuses):
    all_have_been_visited = True
    for i in range(0, size * size):
        if not visited_statuses[i]:
            all_have_been_visited = False
    assert all_have_been_visited
