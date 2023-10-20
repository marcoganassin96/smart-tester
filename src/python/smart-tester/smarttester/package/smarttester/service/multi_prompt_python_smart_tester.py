# imports needed to run the code in this notebook
import ast  # used for detecting whether generated Python code is valid
import os
import time

import openai  # used for calling the OpenAI API

# example of a function that uses a multi-step prompt to write unit tests

from smarttester import PATH_saved_files
from smarttester.service.multi_prompt_data import MultiPromptData
from smarttester.service.dataclass.function_data import FunctionData
from smarttester.utils.messages_printer import print_messages, print_message_delta
from smarttester.utils.text_utils import _get_bullets_number

from smarttester.utils.save_text import save_text_in_saved_files_dir


def explain_tests_from_function(
        multi_prompt_data: MultiPromptData,  # Python function to test, as a string
        print_text: bool = False,  # optionally prints text; helpful for understanding the function & debugging
        explain_model: str = "gpt-3.5-turbo",  # model used to generate text plans in step 1
        temperature: float = 0.4,  # temperature = 0 can sometimes get stuck in repetitive loops, so we use 0.4
) -> (dict[str, str], dict[str, str], dict[str, str]):
    """Returns a unit test for a given Python function, using a 3-step GPT prompt."""

    # Step 1: Generate an explanation of the function

    # create a markdown-formatted message that asks GPT to explain the function, formatted as a bullet list
    explain_system_message = {
        "role": "system",
        "content": """You are a world-class Python developer with an eagle eye for unintended bugs and edge cases. 
        You carefully explain code with great detail and accuracy. You organize your explanations in 
        markdown-formatted, bulleted lists.
        """,
    }

    function_data: FunctionData = multi_prompt_data.get_function_data()
    function_to_test = function_data.function

    explain_user_message = {
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
    explain_messages = [explain_system_message, explain_user_message]
    if print_text:
        print_messages(explain_messages)

    explanation_response = openai.ChatCompletion.create(
        model=explain_model,
        messages=explain_messages,
        temperature=temperature,
        stream=True,
    )
    explanation = ""
    for chunk in explanation_response:
        delta = chunk["choices"][0]["delta"]
        if print_text:
            print_message_delta(delta)
        if "content" in delta:
            explanation += delta["content"]
    explain_assistant_message = {"role": "assistant", "content": explanation}
    return explanation, explain_system_message, explain_user_message, explain_assistant_message


def plan_tests_from_explain(
        explain_system_message: dict[str, str],
        explain_user_message: dict[str, str],
        explain_assistant_message: dict[str, str],
        unit_test_package: str = "pytest",  # unit testing package; use the name as it appears in the import statement
        print_text: bool = False,  # optionally prints text; helpful for understanding the function & debugging
        plan_model: str = "gpt-3.5-turbo",  # model used to generate text plans in steps 2 and 2b
        temperature: float = 0.4,  # temperature = 0 can sometimes get stuck in repetitive loops, so we use 0.4
) -> (str, dict[str, str], dict[str, str]):
    # Asks GPT to plan out cases the units tests should cover, formatted as a bullet list
    plan_user_message = {
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
    plan_messages = [
        explain_system_message,
        explain_user_message,
        explain_assistant_message,
        plan_user_message,
    ]
    if print_text:
        print_messages([plan_user_message])
    plan_response = openai.ChatCompletion.create(
        model=plan_model,
        messages=plan_messages,
        temperature=temperature,
        stream=True,
    )
    plan = ""
    for chunk in plan_response:
        delta = chunk["choices"][0]["delta"]
        if print_text:
            print_message_delta(delta)
        if "content" in delta:
            plan += delta["content"]
    plan_assistant_message = {"role": "assistant", "content": plan}
    return plan, plan_user_message, plan_assistant_message


def increase_plan_tests(
        explain_system_message: dict[str, str],
        explain_user_message: dict[str, str],
        explain_assistant_message: dict[str, str],
        plan_user_message: dict[str, str],
        plan_assistant_message: dict[str, str],
        print_text: bool = False,  # optionally prints text; helpful for understanding the function & debugging
        plan_model: str = "gpt-3.5-turbo",  # model used to generate text plans in steps 2 and 2b
        temperature: float = 0.4,  # temperature = 0 can sometimes get stuck in repetitive loops, so we use 0.4
) -> (str, dict[str, str], dict[str, str]):
    elaboration_user_message = {
        "role": "user",
        "content": f"""In addition to those scenarios above, list a few rare or unexpected edge cases (and as before, under each edge case, include a few examples as sub-bullets).""",
    }
    elaboration_messages = [
        explain_system_message,
        explain_user_message,
        explain_assistant_message,
        plan_user_message,
        plan_assistant_message,
        elaboration_user_message,
    ]
    if print_text:
        print_messages([elaboration_user_message])
    elaboration_response = openai.ChatCompletion.create(
        model=plan_model,
        messages=elaboration_messages,
        temperature=temperature,
        stream=True,
    )
    elaboration = ""
    for chunk in elaboration_response:
        delta = chunk["choices"][0]["delta"]
        if print_text:
            print_message_delta(delta)
        if "content" in delta:
            elaboration += delta["content"]
    elaboration_assistant_message = {"role": "assistant", "content": elaboration}
    return elaboration, elaboration_user_message, elaboration_assistant_message


def generate_tests_form_plan(
        explain_user_message: dict[str, str],
        explain_assistant_message: dict[str, str],
        plan_user_message: dict[str, str],
        plan_assistant_message: dict[str, str],
        function_to_test: str,  # Python function to test, as a string
        elaboration_needed: bool = False,
        elaboration_user_message: dict[str, str] = None,
        elaboration_assistant_message: dict[str, str] = None,
        unit_test_package: str = "pytest",  # unit testing package; use the name as it appears in the import statement
        print_text: bool = False,  # optionally prints text; helpful for understanding the function & debugging
        execute_model: str = "gpt-3.5-turbo",  # model used to generate code in step 3
        temperature: float = 0.4,  # temperature = 0 can sometimes get stuck in repetitive loops, so we use 0.4
) -> str:
    # create a markdown-formatted prompt that asks GPT to complete a unit test
    package_comment = ""
    if unit_test_package == "pytest":
        package_comment = "# below, each test case is represented by a tuple passed to the @pytest.mark.parametrize decorator"
    execute_system_message = {
        "role": "system",
        "content": """You are a world-class Python developer with an eagle eye for unintended bugs and edge cases.
                   You write careful, accurate unit tests. When asked to reply only with code, you write all of your code in a single block.""",
    }
    execute_user_message = {
        "role": "user",
        "content": f"""Using Python and the `{unit_test_package}` package, write a suite of unit tests for the 
        function, following the cases above. Include helpful comments to explain each line. Reply only with code, 
        formatted as follows: ```python # imports import {unit_test_package}  # used for our unit tests 
    {{insert other imports as needed}}

    # function to test
    {function_to_test}

    # unit tests
    {package_comment}
    {{insert unit test code here}}
    ```""",
    }
    execute_messages = [
        execute_system_message,
        explain_user_message,
        explain_assistant_message,
        plan_user_message,
        plan_assistant_message,
    ]
    if elaboration_needed:
        execute_messages += [elaboration_user_message, elaboration_assistant_message]
    execute_messages += [execute_user_message]
    if print_text:
        print_messages([execute_system_message, execute_user_message])

    execute_response = openai.ChatCompletion.create(
        model=execute_model,
        messages=execute_messages,
        temperature=temperature,
        stream=True,
    )
    execution = ""
    for chunk in execute_response:
        delta = chunk["choices"][0]["delta"]
        if print_text:
            print_message_delta(delta)
        if "content" in delta:
            execution += delta["content"]

    # return the unit test as a string
    return execution


def post_process_execution_response(execution: str, programming_language="python",
                                    execute_model="gpt-3.5-turbo") -> str:
    if programming_language == "python" and execute_model == "gpt-3.5-turbo":
        code = execution.split("```python")[1].split("```")[0].strip()
    else:
        code = execution
    return code


def unit_tests_from_function(
        function_to_test: str,  # Python function to test, as a string
        unit_test_package: str = "pytest",  # unit testing package; use the name as it appears in the import statement
        approx_min_cases_to_cover: int = 7,  # minimum number of test case categories to cover (approximate)
        print_text: bool = False,  # optionally prints text; helpful for understanding the function & debugging
        save_text: bool = True,  # optionally save text in file system
        explain_model: str = "gpt-3.5-turbo",  # model used to generate text plans in step 1
        plan_model: str = "gpt-3.5-turbo",  # model used to generate text plans in steps 2 and 2b
        execute_model: str = "gpt-3.5-turbo",  # model used to generate code in step 3
        temperature: float = 0.4,  # temperature = 0 can sometimes get stuck in repetitive loops, so we use 0.4
        reruns_if_fail: int = 1,  # if the output code cannot be parsed, this will re-run the function up to N times
        continue_from_step: int = 0, # restarts the process from a given step; options are 0: "start", 1: "explain", 2: "plan", 3: "plan_more", 4: "execute", 5: "code"
        source_data_dir: str = None,  # directory where data of the previous steps are stored
) -> str:
    """Returns a unit test for a given Python function, using a 3-step GPT prompt."""

    multi_prompt_data = MultiPromptData()

    if continue_from_step < 0:
        raise Exception("continue_from_step must be >= 0")

    if continue_from_step > 6:
        raise Exception("continue_from_step must be <= 6")

    save_dir = None
    if continue_from_step == 0:
        # if we are continuing from step 0, we need initialize the data with the function to test
        multi_prompt_data.init_function_input(function_to_test)

        # Step 0: Start and optionally save function to test
        if save_text:
            function_name = function_to_test.split("def ")[1].split("(")[0]
            if " " in function_name:
                function_name = function_name.split(" ")[0]
            if function_name is None or len(function_name) < 1:
                function_name = "unknown_function"
            save_dir = f"{int(time.time() * 1000)}-{function_name}"
            try:
                file_path = PATH_saved_files / save_dir
                os.mkdir(file_path)
            except OSError:
                raise Exception(f"{file_path} already exists. Check for errors, delete it and try again.")
            save_text_in_saved_files_dir("function", save_dir, function_to_test)
    else:
        save_dir = source_data_dir

    if continue_from_step <= 1:
        # Step 1: Generate an explanation of the function

        if continue_from_step == 1:
            # if we are continuing from step 1, we need to load the data from the saved files
            multi_prompt_data.load_function_data(save_dir)

        explain_response = explain_tests_from_function(multi_prompt_data, print_text, explain_model, temperature)
        explanation, explain_system_message, explain_user_message, explain_assistant_message = explain_response

        if save_text:
            save_text_in_saved_files_dir("explain", save_dir, explanation)

    if continue_from_step <= 2:
        # Step 2: Generate a plan to write a unit test
        plan_response = plan_tests_from_explain(explain_system_message, explain_user_message, explain_assistant_message,
                                                unit_test_package, print_text, plan_model, temperature)
        plan, plan_user_message, plan_assistant_message = plan_response

        if save_text:
            save_text_in_saved_files_dir("plan", save_dir, plan)

    if continue_from_step <= 3:
        # Step 2b: If the plan is short, ask GPT to elaborate further
        # this counts top-level bullets (e.g., categories), but not sub-bullets (e.g., test cases)

        num_bullets = _get_bullets_number(plan)
        elaboration_needed = num_bullets < approx_min_cases_to_cover

        elaboration_user_message, elaboration_assistant_message = None, None
        if elaboration_needed:
            elaboration_response = increase_plan_tests(explain_system_message, explain_user_message,
                                                       explain_assistant_message, plan_user_message, plan_assistant_message,
                                                       print_text, plan_model, temperature)

            elaboration, elaboration_user_message, elaboration_assistant_message = elaboration_response

            if save_text:
                save_text_in_saved_files_dir("elaboration", save_dir, elaboration)

    if continue_from_step <= 4:
        # Step 3: Generate the unit test
        execution_response = generate_tests_form_plan(explain_user_message, explain_assistant_message, plan_user_message,
                                                      plan_assistant_message, function_to_test, elaboration_needed,
                                                      elaboration_user_message,
                                                      elaboration_assistant_message, unit_test_package, print_text,
                                                      execute_model, temperature)

        execution = execution_response

        if save_text:
            save_text_in_saved_files_dir("execution", save_dir, execution)

    if continue_from_step <= 5:
        # Custom post-processing to fix errors
        code = post_process_execution_response(execution_response)

        if save_text:
            save_text_in_saved_files_dir("code", save_dir, code, "py")

    if continue_from_step <= 6:
        # retry if fails
        try:
            ast.parse(code)
        except SyntaxError as e:
            print(f"Syntax error in generated code: {e}")
            if reruns_if_fail > 0:
                print("Rerunning...")
                return unit_tests_from_function(
                    function_to_test=function_to_test,
                    unit_test_package=unit_test_package,
                    approx_min_cases_to_cover=approx_min_cases_to_cover,
                    print_text=print_text,
                    explain_model=explain_model,
                    plan_model=plan_model,
                    execute_model=execute_model,
                    temperature=temperature,
                    reruns_if_fail=reruns_if_fail - 1,  # decrement rerun counter when calling again
                    continue_from_step=continue_from_step
                )

    # return the unit test as a string
    return code
