from smarttester.service.dataclass.explain_data import ExplainData
from smarttester.service.dataclass.function_data import FunctionData
from smarttester.utils.save_text import load_file_from_saved_files_dir


class MultiPromptData:
    def __init__(self):
        self.function_data: FunctionData = FunctionData()
        self.explain_data: ExplainData = ExplainData()

    # Function data

    def init_function_input(self, function_to_test: str) -> str:
        self.function_data.function = function_to_test
        return function_to_test

    def get_function_data(self) -> FunctionData:
        return self.function_data
    
    # Explain data

    def init_explain_input(self, function_to_test: str) -> tuple[dict[str, str], : dict[str, str]]:
        # create a markdown-formatted message that asks GPT to explain the function, formatted as a bullet list
        self.explain_data.explain_system_message: dict[str, str] = {
            "role": "system",
            "content": """You are a world-class Python developer with an eagle eye for unintended bugs and edge cases. 
                You carefully explain code with great detail and accuracy. You organize your explanations in 
                markdown-formatted, bulleted lists.
                """,
        }
        self.explain_data.explain_user_message: dict[str, str] = {
            "role": "user",
            "content": f"""
                    Please explain the following Python function.
                    Review what each element of the function is doing precisely and what the author's intentions may have been.
                    Organize your explanation as a markdown-formatted, bulleted list.
                    ```python
                    {function_to_test}
                    ```
                """,
        }
        return self.explain_data.explain_system_message, self.explain_data.explain_user_message

    def init_explain_output(self, explanation: str) -> dict[str, str]:
        self.explain_data.explanation = explanation
        self.explain_data.explain_assistant_message = {"role": "assistant", "content": explanation}
        return self.explain_data.explain_assistant_message

    def get_explain_data(self) -> ExplainData:
        return self.explain_data

    # Load data from file system

    def load_function_data(self, saved_dir: str) -> FunctionData:
        function = load_file_from_saved_files_dir(saved_dir=saved_dir, file_name="function", ext="txt")
        self.function_data.function = function
        return self.function_data

    def load_explain_data(self, saved_dir: str) -> ExplainData:
        self.function_data = self.load_function_data(saved_dir=saved_dir)
        self.init_explain_input(function_to_test=self.function_data.function)
        explanation = load_file_from_saved_files_dir(saved_dir=saved_dir, file_name="explain", ext="txt")
        self.init_explain_output(explanation=explanation)
        return self.explain_data
