import pytest
from src.events.event import EventType
from src.maze_solving.dijkstra import Dijkstra
import src.maze_solving.tests.helpers as helpers

TEST_MAZE_0 = [[3], [4], [5], [4, 0, 6], [1, 3, 5], [8, 4, 2], [7, 3], [6], [5]]
PERMANENT_NODES_0 = [0, 3, 4, 6, 1, 5, 7, 2, 8]
BLINK_NODES_0 = [3, 4, 0, 6, 1, 3, 5, 7, 3, 4, 8, 4, 2, 6, 5, 5]
PATH_NODES_0 = [0, 3, 4, 5, 8]

TEST_MAZE_1 = [[1, 3], [0, 4, 2], [1, 5], [0], [7, 1], [2, 8], [7], [4, 6], [5]]
EXPECTED_PATH_1 = [0, 1, 2, 5, 8]

TEST_MAZE_2 = [
    [4],
    [2],
    [6, 1],
    [7],
    [5, 0],
    [4, 9],
    [2, 7],
    [6, 3, 11],
    [9, 12],
    [8, 5],
    [14, 11],
    [10, 7],
    [13, 8],
    [12, 14],
    [10, 13, 15],
    [14],
]
EXPECTED_PATH_2 = [0, 4, 5, 9, 8, 12, 13, 14, 15]

TEST_MAZE_3 = [
    [4],
    [2, 5],
    [1, 6],
    [7],
    [0, 5, 8],
    [4, 1],
    [7, 2, 10],
    [6, 3, 11],
    [9, 4],
    [8, 13],
    [14, 6],
    [7, 15],
    [13],
    [9, 12],
    [10],
    [11],
]
EXPECTED_PATH_3 = [0, 4, 5, 1, 2, 6, 7, 11, 15]


def test_dijkstra_publishes_expected_events_when_traversing_the_maze(mocker):
    spy = mocker.spy(helpers, "dispatch_event")
    dead_end_filler = Dijkstra(TEST_MAZE_0, helpers.dispatch_event)
    dead_end_filler.solve()
    permanent_nodes = []
    blink_nodes = []
    path_nodes = []
    for call in spy.call_args_list:
        event = call[0][0]
        event_type = event.algorithm_event_type
        assert event_type in [
            EventType.PERMANENT_NODE,
            EventType.PATH_NODE,
            EventType.SOLVING_COMPLETED,
            EventType.BLINK_NODE,
        ]
        node = event.nodes[0] if not event_type == EventType.SOLVING_COMPLETED else None
        if event_type == EventType.PERMANENT_NODE:
            permanent_nodes.append(node)
        elif event_type == EventType.PATH_NODE:
            path_nodes.append(node)
    for index, node in enumerate(permanent_nodes):
        assert node == PERMANENT_NODES_0[index]
    for index, node in enumerate(blink_nodes):
        assert node == BLINK_NODES_0[index]
    for index, node in enumerate(path_nodes):
        assert node == PATH_NODES_0[index]


@pytest.mark.parametrize(
    "test_maze,expected_path",
    [
        (TEST_MAZE_1, EXPECTED_PATH_1),
        (TEST_MAZE_2, EXPECTED_PATH_2),
        (TEST_MAZE_3, EXPECTED_PATH_3),
    ],
)
def test_test_dijkstra_solves_maze_correctly(mocker, test_maze, expected_path):
    spy = mocker.spy(helpers, "dispatch_event")
    dead_end_filler = Dijkstra(test_maze, helpers.dispatch_event)
    dead_end_filler.solve()
    nodes_filled = []
    path_nodes = []
    for call in spy.call_args_list:
        event = call[0][0]
        event_type = event.algorithm_event_type
        assert event_type in [
            EventType.PERMANENT_NODE,
            EventType.BLINK_NODE,
            EventType.PATH_NODE,
            EventType.SOLVING_COMPLETED,
        ]
        node = event.nodes[0] if not event_type == EventType.SOLVING_COMPLETED else None
        if event_type == EventType.PERMANENT_NODE:
            nodes_filled.append(node)
        elif event_type == EventType.PATH_NODE:
            path_nodes.append(node)
    for index, node in enumerate(path_nodes):
        assert node == expected_path[index]
