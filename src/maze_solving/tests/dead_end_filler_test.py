import pytest
from src.events.event import EventType
from src.maze_solving.dead_end_filler import DeadEndFiller
import src.maze_solving.tests.helpers as helpers

TEST_MAZE_1 = [[1, 3], [0, 4, 2], [1, 5], [0], [7, 1], [2, 8], [7], [4, 6], [5]]
EXPECTED_FILLS_1 = [3, 6, 7, 4]
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
EXPECTED_FILLS_2 = [1, 2, 6, 3, 7, 11, 10]
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
EXPECTED_FILLS_3 = [3, 12, 13, 9, 8, 14, 10]
EXPECTED_PATH_3 = [0, 4, 5, 1, 2, 6, 7, 11, 15]


@pytest.mark.parametrize(
    "test_maze,expected_fills,expected_path",
    [
        (TEST_MAZE_1, EXPECTED_FILLS_1, EXPECTED_PATH_1),
        (TEST_MAZE_2, EXPECTED_FILLS_2, EXPECTED_PATH_2),
        (TEST_MAZE_3, EXPECTED_FILLS_3, EXPECTED_PATH_3),
    ],
)
def test_dead_end_filler_publishes_expected_events_when_traversing_the_maze(
    mocker, test_maze, expected_fills, expected_path
):
    spy = mocker.spy(helpers, "dispatch_event")
    dead_end_filler = DeadEndFiller(test_maze, helpers.dispatch_event)
    dead_end_filler.solve()
    nodes_filled = []
    path_nodes = []
    for call in spy.call_args_list:
        event = call[0][0]
        event_type = event.algorithm_event_type
        assert event_type in [
            EventType.PERMANENT_NODE,
            EventType.PATH_NODE,
            EventType.SOLVING_COMPLETED,
        ]
        node = event.nodes[0] if not event_type == EventType.SOLVING_COMPLETED else None
        if event_type == EventType.PERMANENT_NODE:
            nodes_filled.append(node)
        elif event_type == EventType.PATH_NODE:
            path_nodes.append(node)
    for index, node in enumerate(nodes_filled):
        assert node == expected_fills[index]
    for index, node in enumerate(path_nodes):
        assert node == expected_path[index]
