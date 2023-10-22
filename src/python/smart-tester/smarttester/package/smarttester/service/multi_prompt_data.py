from smarttester.service.dataclass.elaboration_data import ElaborationData
from smarttester.service.dataclass.execution_data import ExecutionData
from smarttester.service.dataclass.function_data import FunctionData
from smarttester.service.dataclass.explain_data import ExplainData
from smarttester.service.dataclass.plan_data import PlanData
from smarttester.service.dataclass.post_processing_data import PostProcessingData
from smarttester.utils.save_text import load_file_from_saved_files_dir


class MultiPromptData:
    def __init__(self):
        self.function_data: FunctionData = FunctionData()
        self.explain_data: ExplainData = ExplainData()
        self.plan_data: PlanData = PlanData()
        self.elaboration_data: ElaborationData = ElaborationData()
        self.execution_data: ExecutionData = ExecutionData()
        self.post_processing_data: PostProcessingData = PostProcessingData

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

    # Plan data

    def init_plan_input(self, unit_test_package: str) -> tuple[dict[str, str], list[dict[str, str]]]:
        self.plan_data.plan_user_message = {
            "role": "user",
            "content": f"""A good unit test suite should aim to:
            - Test the function's behavior for a wide range of possible inputs
            - Test edge cases that the author may not have foreseen
            - Take advantage of the features of `{unit_test_package}` to make the tests easy to write and maintain
            - Be easy to read and understand, with clean code and descriptive names
            - Be deterministic, so that the tests always pass or fail in the same way
            To help unit test the function above, list diverse scenarios that the function should be able to handle
            (and under each scenario, include a few examples as sub-bullets).""",
        }

        explain_data: ExplainData = self.explain_data
        plan_messages: list[dict[str, str]] = [
            explain_data.explain_system_message,
            explain_data.explain_user_message,
            explain_data.explain_assistant_message,
            self.plan_data.plan_user_message,
        ]

        return self.plan_data.plan_user_message, plan_messages

    def init_plan_output(self, plan: str) -> dict[str, str]:
        self.plan_data.plan = plan
        self.plan_data.plan_assistant_message = {"role": "assistant", "content": plan}
        return self.plan_data.plan_assistant_message

    def get_plan_data(self) -> PlanData:
        return self.plan_data

    # Elaboration data

    def init_elaboration_input(self) -> dict[str, str]:

        self.elaboration_data.elaboration_user_message = {
            "role": "user",
            "content": f"""In addition to those scenarios above, list a few rare or unexpected edge cases (and as before, under each edge case, include a few examples as sub-bullets).""",
        }
        self.elaboration_data.elaboration_needed = True
        return self.elaboration_data.elaboration_user_message

    def init_elaboration_output(self, elaboration: str) -> dict[str, str]:
        self.elaboration_data.elaboration = elaboration
        self.elaboration_data.elaboration_assistant_message = {"role": "assistant", "content": elaboration}

    def get_elaboration_data(self) -> ElaborationData:
        return self.elaboration_data

    # Execution data

    def init_execution_input(self, unit_test_package) -> dict[str, str]:
        package_comment = ""
        if unit_test_package == "pytest":
            package_comment = "# below, each test case is represented by a tuple passed to the @pytest.mark.parametrize decorator"

        self.execution_data.execute_system_message = {
            "role": "system",
            "content": """You are a world-class Python developer with an eagle eye for unintended bugs and edge cases.
                       You write careful, accurate unit tests. When asked to reply only with code, you write all of your code in a single block.""",
        }

        self.execution_data.execute_user_message = {
            "role": "user",
            "content": f"""Using Python and the `{unit_test_package}` package, write a suite of unit tests for the 
            function, following the cases above. Include helpful comments to explain each line. Reply only with code, 
            formatted as follows: ```python # imports import {unit_test_package}  # used for our unit tests 
        {{insert other imports as needed}}

        # function to test
        
        {self.function_data.function}

        # unit tests
        {package_comment}
        {{insert unit test code here}}
        ```""",
        }
        return self.execution_data.execute_system_message, self.execution_data.execute_user_message

    def init_execution_output(self, execution: str) -> dict[str, str]:
        self.execution_data.execution = execution

    def get_execution_data(self) -> ExecutionData :
        return self.execution_data

    # Post processing data

    def init_post_processing_output(self, code: str):
        self.post_processing_data.code = code

    def get_post_processing_data(self) -> PostProcessingData:
        return self.post_processing_data

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

    def load_plan_data(self, saved_dir: str, unit_test_package="pytest") -> PlanData:
        self.explain_data = self.load_explain_data(saved_dir=saved_dir)
        self.init_plan_input(unit_test_package=unit_test_package)
        plan = load_file_from_saved_files_dir(saved_dir=saved_dir, file_name="plan", ext="txt")
        self.init_plan_output(plan=plan)
        return self.plan_data

    def load_elaboration_data(self, saved_dir: str, unit_test_package="pytest") -> ElaborationData:
        self.load_plan_data(saved_dir=saved_dir, unit_test_package=unit_test_package)

        try:  # elaboration is optional
            elaboration = load_file_from_saved_files_dir(saved_dir=saved_dir, file_name="elaboration", ext="txt")
            self.init_elaboration_input()
            self.init_elaboration_output(elaboration=elaboration)
        except FileNotFoundError:
            self.elaboration_data = ElaborationData(elaboration_needed=False)

        return self.elaboration_data

    def load_execution_data(self, saved_dir: str, unit_test_package="pytest") -> ExecutionData:
        self.load_elaboration_data(saved_dir=saved_dir, unit_test_package=unit_test_package)
        self.init_execution_input(unit_test_package=unit_test_package)
        execution = load_file_from_saved_files_dir(saved_dir=saved_dir, file_name="execution", ext="txt")
        self.init_execution_output(execution=execution)
        return self.execution_data

    def load_post_processing_data(self, saved_dir: str, unit_test_package="pytest") -> PostProcessingData:
        self.load_execution_data(saved_dir=saved_dir, unit_test_package=unit_test_package)
        code = load_file_from_saved_files_dir(saved_dir=saved_dir, file_name="code", ext="py")
        self.init_post_processing_output(code=code)
        return self.post_processing_data

