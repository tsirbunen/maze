from src.utils.logger import Logger

class InputGetter:
    def __init__(self):
        self.logger = Logger()

    def get_valid_input(self, question, validate_fn, error) -> str:
        while True:
            answer = self.get_input(question)
            if validate_fn(answer):
                return answer
            self.logger.logYellow(error)

    # Method cannot be made private because we want to mock it in tests!
    def get_input(self, question):
        return input(f"\033[94m\t{question}\033[00m")
