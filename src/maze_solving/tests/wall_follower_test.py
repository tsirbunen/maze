import pytest
from src.events.event import EventType
from src.maze_solving.tests.helpers import dispatch_event
from src.maze_solving.wall_follower import Side, WallFollower
import src.maze_solving.tests.helpers as helpers

TEST_MAZE_1 = [[1, 3], [0, 4, 2], [1, 5], [0], [7, 1], [2, 8], [7], [4, 6], [5]]
EXPECTED_PATH_1 = [0, 3, 0, 1, 4, 7, 6, 7, 4, 1, 2, 5, 8]

TEST_MAZE_2 = [
    [1, 4],
    [5, 0],
    [3],
    [2, 7],
    [0],
    [1, 9],
    [7],
    [6, 11, 3],
    [9, 12],
    [5, 8, 10],
    [11, 14, 9],
    [7, 10],
    [8],
    [14],
    [13, 10, 15],
    [14],
]
EXPECTED_ROUTE_2 = [0, 4, 0, 1, 5, 9, 8, 12, 8, 9, 10, 14, 13, 14, 15]
EXPECTED_PATH_2 = [0, 1, 5, 9, 10, 14, 15]

TEST_MAZE_3 = [
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
EXPECTED_ROUTE_3 = [0, 4, 5, 9, 8, 12, 13, 14, 15]
EXPECTED_PATH_3 = [0, 4, 5, 9, 8, 12, 13, 14, 15]

TEST_MAZE_4 = [
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
EXPECTED_ROUTE_4 = [
    0,
    4,
    8,
    9,
    13,
    12,
    13,
    9,
    8,
    4,
    5,
    1,
    2,
    6,
    10,
    14,
    10,
    6,
    7,
    11,
    15,
]
EXPECTED_PATH_4 = [0, 4, 5, 1, 2, 6, 7, 11, 15]


@pytest.mark.parametrize(
    "test_maze,expected_route,expected_path",
    [
        (TEST_MAZE_2, EXPECTED_ROUTE_2, EXPECTED_PATH_2),
        (TEST_MAZE_3, EXPECTED_ROUTE_3, EXPECTED_PATH_3),
        (TEST_MAZE_4, EXPECTED_ROUTE_4, EXPECTED_PATH_4),
    ],
)
def test_wall_follower_publishes_expected_events_when_traversing_the_maze(
    mocker, test_maze, expected_route, expected_path
):
    spy = mocker.spy(helpers, "dispatch_event")
    wall_follower = WallFollower(test_maze, helpers.dispatch_event)
    wall_follower.solve()
    nodes_in_route = []
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
            nodes_in_route.append(node)
        elif event_type == EventType.PATH_NODE:
            path_nodes.append(node)
    for index, node in enumerate(nodes_in_route):
        assert node == expected_route[index]
    for index, node in enumerate(path_nodes):
        assert node == expected_path[index]


def test_wall_follower_turns_correctly():
    wall_follower = WallFollower(TEST_MAZE_1, dispatch_event)
    wall_follower._turn_right()
    node_in_front = wall_follower._get_node_in_front()
    assert node_in_front == 3
    wall_follower._go_forward()
    assert wall_follower.current_node == 3
    assert wall_follower.facing == Side.DOWN

    wall_follower._turn_right()
    assert not wall_follower._can_go_forward()
    wall_follower._turn_left()
    assert not wall_follower._can_go_forward()
    wall_follower._turn_left()
    assert not wall_follower._can_go_forward()
    wall_follower._turn_left()
    node_in_front = wall_follower._get_node_in_front()
    assert node_in_front == 0
    wall_follower._go_forward()
    assert wall_follower.current_node == 0
    assert wall_follower.facing == Side.UP

    wall_follower._turn_right()
    node_in_front = wall_follower._get_node_in_front()
    assert node_in_front == 1
    wall_follower._go_forward()
    assert wall_follower.current_node == 1
    assert wall_follower.facing == Side.RIGHT

    wall_follower._turn_right()
    node_in_front = wall_follower._get_node_in_front()
    assert node_in_front == 4
    wall_follower._go_forward()
    assert wall_follower.current_node == 4
    assert wall_follower.facing == Side.DOWN
