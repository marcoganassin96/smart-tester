# imports needed to run the code in this notebook
import ast  # used for detecting whether generated Python code is valid
import json
import os
import time

import openai  # used for calling the OpenAI API

# example of a function that uses a multi-step prompt to write unit tests

from smarttester import PATH_saved_files
from smarttester.service.dataclass.elaboration_data import ElaborationData
from smarttester.service.dataclass.execution_data import ExecutionData
from smarttester.service.dataclass.multi_step_data import MultiStepData
from smarttester.service.dataclass.plan_data import PlanData
from smarttester.service.multi_prompt_data import MultiPromptData
from smarttester.service.dataclass.function_data import FunctionData
from smarttester.service.dataclass.explain_data import ExplainData
from smarttester.utils.messages_printer import print_messages, print_message_delta
from smarttester.utils.text_utils import _get_bullets_number

from smarttester.utils.save_text import save_text_in_saved_files_dir


def explain_tests_from_function(
        multi_prompt_data: MultiPromptData,  # input and output data structure
        print_text: bool = False,  # optionally prints text; helpful for understanding the function & debugging
        explain_model: str = "gpt-3.5-turbo",  # model used to generate text plans in step 1
        temperature: float = 0.4,  # temperature = 0 can sometimes get stuck in repetitive loops, so we use 0.4,
) -> str:
    """Returns a unit test for a given Python function, using a 3-step GPT prompt."""

    function_data: FunctionData = multi_prompt_data.get_function_data()
    function_to_test = function_data.function

    explain_system_message, explain_user_message = multi_prompt_data.init_explain_input(function_to_test)

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

    multi_prompt_data.init_explain_output(explanation)

    return explanation


def plan_tests_from_explain(
        multi_prompt_data: MultiPromptData,  # input and output data structure
        print_text: bool = False,  # optionally prints text; helpful for understanding the function & debugging
        plan_model: str = "gpt-3.5-turbo",  # model used to generate text plans in steps 2 and 2b
        temperature: float = 0.4,  # temperature = 0 can sometimes get stuck in repetitive loops, so we use 0.4
) -> str:
    # Asks GPT to plan out cases the units tests should cover, formatted as a bullet list

    plan_user_message, plan_messages = multi_prompt_data.init_plan_input()

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

    multi_prompt_data.init_plan_output(plan)

    return plan


def increase_plan_tests(
        multi_prompt_data: MultiPromptData,  # input and output data structure
        print_text: bool = False,  # optionally prints text; helpful for understanding the function & debugging
        plan_model: str = "gpt-3.5-turbo",  # model used to generate text plans in steps 2 and 2b
        temperature: float = 0.4,  # temperature = 0 can sometimes get stuck in repetitive loops, so we use 0.4
) -> (str, dict[str, str], dict[str, str]):
    explain_data = multi_prompt_data.get_explain_data()
    plan_data = multi_prompt_data.get_plan_data()
    elaboration_user_message = multi_prompt_data.init_elaboration_input()

    elaboration_messages = [
        explain_data.explain_system_message,
        explain_data.explain_user_message,
        explain_data.explain_assistant_message,
        plan_data.plan_user_message,
        plan_data.plan_assistant_message,
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

    multi_prompt_data.init_elaboration_output(elaboration)

    return elaboration



def generate_tests_form_plan(
        multi_prompt_data: MultiPromptData,  # input and output data structure
        print_text: bool = False,  # optionally prints text; helpful for understanding the function & debugging
        execute_model: str = "gpt-3.5-turbo",  # model used to generate code in step 3
        temperature: float = 0.4,  # temperature = 0 can sometimes get stuck in repetitive loops, so we use 0.4
) -> str:
    # create a markdown-formatted prompt that asks GPT to complete a unit test

    execute_system_message, execute_user_message = multi_prompt_data.init_execution_input()

    explain_data: ExplainData = multi_prompt_data.get_explain_data()
    plan_data: PlanData = multi_prompt_data.plan_data

    execute_messages = [
        execute_system_message,
        explain_data.explain_user_message,
        explain_data.explain_assistant_message,
        plan_data.plan_user_message,
        plan_data.plan_assistant_message,
    ]

    elaboration_data: ElaborationData = multi_prompt_data.get_elaboration_data()

    if elaboration_data.elaboration_needed:
        execute_messages += [
            elaboration_data.elaboration_user_message,
            elaboration_data.elaboration_assistant_message
        ]
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

    multi_prompt_data.init_execution_output(execution)
    # return the unit test as a string
    return execution


def post_process_execution_response(multi_prompt_data: MultiPromptData,
                                    execute_model="gpt-3.5-turbo") -> str:
    function_data: FunctionData = multi_prompt_data.get_function_data()
    execution_data: ExecutionData = multi_prompt_data.get_execution_data()
    if function_data.programming_language == "python" and execute_model == "gpt-3.5-turbo":
        code = execution_data.execution.split("```python")[1].split("```")[0].strip()
    else:
        code = execution_data.execution
    return code


def unit_tests_from_function(
        function_to_test: str,  # Function to test, as a string
        programming_language: str = "python",  # programming language of the function to test
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

    # start from here to lod multi_step_data_input

    if continue_from_step < 0:
        raise Exception("continue_from_step must be >= 0")

    if continue_from_step > 6:
        raise Exception("continue_from_step must be <= 6")

    save_dir = None

    # Step 0: Start and optionally save function to test

    if continue_from_step == 0:
        # if we are continuing from step 0, we need initialize the data with the function to test

        function_name = function_to_test.split("def ")[1].split("(")[0]
        if " " in function_name:
            function_name = function_name.split(" ")[0]
        if function_name is None or len(function_name) < 1:
            function_name = "unknown_function"

        multi_prompt_data.init_function_input(function_to_test, function_name, programming_language, unit_test_package)

        multi_prompt_data.init_multi_step_data_input(explain_model, plan_model, execute_model)

        # Step 0: Start and optionally save function to test
        if save_text:
            save_dir = f"{int(time.time() * 1000)}-{function_name}"
            try:
                file_path = PATH_saved_files / save_dir
                os.mkdir(file_path)
            except OSError:
                raise Exception(f"{file_path} already exists. Check for errors, delete it and try again.")
            save_text_in_saved_files_dir("function", save_dir, function_to_test)

            function_metadata = {
                "function_name": function_name,
                "programming_language": programming_language,
                "unit_test_package": unit_test_package
            }
            function_metadata_json = json.dumps(function_metadata)
            save_text_in_saved_files_dir("function_metadata", save_dir, function_metadata_json, ext="json")

            # save the multi_step_data as json file
            multi_step_data: MultiStepData = multi_prompt_data.get_multi_step_data()
            multi_step_data_json = multi_step_data.to_json()
            save_text_in_saved_files_dir("multistep_data", save_dir, multi_step_data_json, "json")
    else:
        save_dir = source_data_dir

    if continue_from_step <= 1:
        # Step 1: Generate an explanation of the function

        if continue_from_step == 1:
            # if we are continuing from step 1, we need to load the data from the saved files
            multi_prompt_data.load_function_data(save_dir)
            multi_prompt_data.load_multi_step_data(save_dir)

        explanation = explain_tests_from_function(multi_prompt_data, print_text, explain_model, temperature)

        if save_text:
            save_text_in_saved_files_dir("explain", save_dir, explanation)

    if continue_from_step <= 2:
        # Step 2: Generate a plan to write a unit test

        if continue_from_step == 2:
            # if we are continuing from step 2, we need to load the data from the saved files
            multi_prompt_data.load_explain_data(save_dir)
            
        plan: str = plan_tests_from_explain(multi_prompt_data, print_text, plan_model, temperature)

        if save_text:
            save_text_in_saved_files_dir("plan", save_dir, plan)

    if continue_from_step <= 3:
        # Step 2b: If the plan is short, ask GPT to elaborate further

        if continue_from_step == 3:
            multi_prompt_data.load_plan_data(save_dir)

        # this counts top-level bullets (e.g., categories), but not sub-bullets (e.g., test cases)

        plan = multi_prompt_data.get_plan_data().plan
        num_bullets = _get_bullets_number(plan)
        elaboration_needed = num_bullets < approx_min_cases_to_cover

        if elaboration_needed:
            elaboration = increase_plan_tests(multi_prompt_data, print_text, plan_model, temperature)

            if save_text:
                save_text_in_saved_files_dir("elaboration", save_dir, elaboration)

    if continue_from_step <= 4:

        # Step 3: Generate the unit test

        if continue_from_step == 4:
            multi_prompt_data.load_elaboration_data(save_dir)

        execution = generate_tests_form_plan(multi_prompt_data, print_text,
                                             execute_model, temperature)

        if save_text:
            save_text_in_saved_files_dir("execution", save_dir, execution)

    if continue_from_step <= 5:
        # Custom post-processing to fix errors

        if continue_from_step == 5:
            multi_prompt_data.load_execution_data(save_dir)

        code = post_process_execution_response(multi_prompt_data)

        multi_prompt_data.init_post_processing_output(code)

        if save_text:
            save_text_in_saved_files_dir("code", save_dir, code, "py")

    if continue_from_step <= 6:
        # retry if fails

        if continue_from_step == 6:
            multi_prompt_data.load_post_processing_data(save_dir)
        try:
            post_processing_data = multi_prompt_data.get_post_processing_data()
            ast.parse(post_processing_data.code)
            # return the unit test as a string
            return post_processing_data.code
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
    function_data: FunctionData = multi_prompt_data.get_function_data()
    raise Exception(f"""Cannot generate a valid unit test for the current function {function_data.function_name} after {reruns_if_fail} attempts.
    Check the partial results in the directory {save_dir}.""")
