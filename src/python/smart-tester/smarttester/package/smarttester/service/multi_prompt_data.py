from smarttester.service.dataclass.function_data import FunctionData
from smarttester.utils.save_text import load_file_from_saved_files_dir


class MultiPromptData:
    def __init__(self):
        self.function_data: FunctionData = FunctionData()

    # Function data

    def init_function_input(self, function_to_test: str) -> str:
        self.function_data.function = function_to_test
        return function_to_test

    def get_function_data(self) -> FunctionData:
        return self.function_data

    # Load data from file system

    def load_function_data(self, saved_dir: str) -> FunctionData:
        function = load_file_from_saved_files_dir(saved_dir=saved_dir, file_name="function", ext="txt")
        self.function_data.function = function
        return self.function_data
