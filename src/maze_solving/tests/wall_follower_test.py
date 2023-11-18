from src.events.event import EventType
from src.maze_solving.tests.helpers import dispatch_event
from src.maze_solving.wall_follower import Side, WallFollower
import src.maze_solving.tests.helpers as helpers

TEST_MAZE = [[1, 3], [0, 4, 2], [1, 5], [0], [7, 1], [2, 8], [7], [4, 6], [5]]
EXPECTED_PATH = [0, 3, 0, 1, 4, 7, 6, 7, 4, 1, 2, 5, 8]


def test_wall_follower_turns_correctly():
    wall_follower = WallFollower(TEST_MAZE, dispatch_event)
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


def test_wall_follower_publishes_expected_events_when_traversing_the_maze(mocker):
    spy = mocker.spy(helpers, "dispatch_event")
    wall_follower = WallFollower(TEST_MAZE, helpers.dispatch_event)
    wall_follower.solve()
    nodes_path = []
    for call in spy.call_args_list:
        event = call[0][0]
        assert event.algorithm_event_type == EventType.PERMANENT_NODE
        node = event.nodes[0]
        nodes_path.append(node)

    for index, node in enumerate(nodes_path):
        assert node == EXPECTED_PATH[index]
