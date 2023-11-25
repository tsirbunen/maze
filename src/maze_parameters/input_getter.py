from src.utils.logger import Logger


class InputGetter:
    """Gets single input from the user and validates it."""

    def __init__(self):
        self.logger = Logger()

    def get_valid_input(self, question, validate_fn, error) -> str:
        """Performs querying the user for single input and validates it."""
        while True:
            answer = self._get_input(question)
            if validate_fn(answer):
                return answer
            self.logger.log_yellow(error)

    def _get_input(self, question):
        return input(f"\033[94m\t{question}\033[00m")
