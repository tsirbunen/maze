from io import StringIO
# We cannot use the regular imports like "from .parameters_querier import ParametersQuerier"
# because those cannot be mocked. So instead, we import like this:
import src.maze_parameters.parameters_querier as p
import src.maze_parameters.maze_type as t
from src.maze_parameters.constants import WELCOME_TITLE

mock_input = "src.maze_parameters.parameters_querier.ParametersQuerier.get_input"
querier = p.ParametersQuerier()
single = t.MazeType.SINGLE
multiple = t.MazeType.MULTIPLE

def test_instructions_are_printed_to_console(capsys, mocker):
    spy = mocker.spy(querier, "log_instructions")
    assert spy.call_count == 0
    querier.log_instructions()
    captured = capsys.readouterr()
    assert spy.call_count == 1
    assert WELCOME_TITLE in captured.out


def test_size_validation_valid_input():
    valid_sizes = [2, 3, 17, 33, 49, 50]
    for size in valid_sizes:
        assert querier.is_valid_size(size)

def test_size_validation_invalid_input():
    invalid_sizes = [1, 51, 0, -1, 'x']
    for size in invalid_sizes:
        assert not querier.is_valid_size(size)

def test_type_validation_valid_input():
    valid_types = ['s', 'm']
    for maze_type in valid_types:
        assert querier.is_valid_type(maze_type)

def test_type_validation_invalid_input():
    invalid_types = ['x', 'C', 33]
    for maze_type in invalid_types:
        assert not querier.is_valid_type(maze_type)

def test_get_size_valid_input(monkeypatch):
    valid_answers = [("33", 33), ("2", 2), ("50", 50)]
    for item in valid_answers:
        monkeypatch.setattr('sys.stdin', StringIO(f"{item[0]}\n"))
        size = querier.get_size()
        assert size == item[1]

def test_get_size_first_invalid_then_valid_input(mocker):
    user_input = ["1", "7"]
    mocker.patch(mock_input, side_effect=user_input)
    size = querier.get_size()
    assert size == int(user_input[1])

def test_get_type_valid_input(monkeypatch):
    valid_answers = [("s", single), ("m", multiple)]
    for item in valid_answers:
        monkeypatch.setattr('sys.stdin', StringIO(f"{item[0]}\n"))
        size = querier.get_type()
        assert size == item[1]

def test_get_type_first_invalid_then_valid_input(mocker):
    user_input = ["w", "m"]
    mocker.patch(mock_input, side_effect=user_input)
    maze_type = querier.get_type()
    assert maze_type == t.MazeType.MULTIPLE

def test_get_parameters_valid_input(mocker):
    user_input = ["33", "s"]
    mocker.patch(mock_input, side_effect=user_input)
    parameters = querier.get_parameters()
    assert parameters.mazeType == single
