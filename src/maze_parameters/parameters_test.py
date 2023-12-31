from src.maze_parameters.parameters_querier import ParametersQuerier
from src.maze_parameters.constants import WELCOME_TITLE
from src.maze_parameters.maze_type import MazeType

MOCK_INPUT = "src.maze_parameters.input_getter.InputGetter._get_input"
querier = ParametersQuerier()
single = MazeType.SINGLE
multiple = MazeType.MULTIPLE


def test_instructions_are_printed_to_console(capsys):
    querier._log_instructions()
    captured = capsys.readouterr()
    assert WELCOME_TITLE in captured.out


def test_size_validation_with_valid_input_returns_true():
    valid_sizes = [2, 3, 17, 20]
    for size in valid_sizes:
        assert querier._validate_maze_size(size)


def test_size_validation_with_invalid_input_returns_false():
    invalid_sizes = [1, 21, 0, -1, "x"]
    for size in invalid_sizes:
        assert not querier._validate_maze_size(size)


def test_type_validation_with_valid_input_returns_true():
    valid_types = ["s", "m"]
    for maze_type in valid_types:
        assert querier._validate_maze_type(maze_type)


def test_type_validation_with_invalid_input_returns_false():
    invalid_types = ["x", "C", 18]
    for maze_type in invalid_types:
        assert not querier._validate_maze_type(maze_type)


def test_size_is_queried_until_valid_input_value_is_given(mocker):
    user_input = ["1", "21", "0", "7"]
    mocker.patch(MOCK_INPUT, side_effect=user_input)
    size = querier._get_size()
    assert size == int(user_input[len(user_input) - 1])


def test_type_is_queried_until_valid_input_value_is_given(mocker):
    user_input = ["w", 1, "ss", "m"]
    mocker.patch(MOCK_INPUT, side_effect=user_input)
    maze_type = querier._get_type()
    assert maze_type == MazeType.MULTIPLE


def test_querier_returns_valid_parameter_values(mocker):
    user_input_expected_output_tuples = [
        (["m", "999", "19", "s"], [19, single]),
        (["1", "22", "14", "w", "mm", "m"], [14, multiple]),
    ]
    for user_input, expected_output in user_input_expected_output_tuples:
        mocker.patch(MOCK_INPUT, side_effect=user_input)
        parameters = querier.get_parameters()
        assert parameters.size == expected_output[0]
        assert parameters.maze_type == expected_output[1]
