# Smart Tester

![alt text](https://github.com/marcoganassin96/smart-tester/blob/update/readme/assets/bugs_hunter.png)

### A unit test function/classes generator for Python/Java
Smart Tester provides the generation of unit tests for the given functions, through multi-step prompts to an LLM.

This approach is inspired by "Unit test writing using a multi-step prompt" by Ted Sanders (https://github.com/ted-at-openai), from the official OpenAI Cookbook on Github (https://github.com/openai/openai-cookbook/blob/main/examples/Unit_test_writing_using_a_multi-step_prompt.ipynb).

As suggested by the CookBook, 4 base steps are provided:
1. Explain: Given a Python function, we ask GPT to explain what the function is doing and why..
2. Plan: We ask GPT to plan a set of unit tests for the function.
3. If the plan is too short, we ask GPT to elaborate with more ideas for unit tests.
4. Execute: Finally, we instruct GPT to write unit tests that cover the planned cases.

In this project 2 additional steps are structured:
5. Post-processing: Fix common errors produced by the LLM-generated unit test code
6. Verify: Verify if the post-processed code is executable

### Provided functionalities
- Develop an LLM-based service to generate test functions for Python, with pytest (and pytest.mark.parametrize)
- Saved intermediate steps in persistent files to review step outputs and restart computation from an intermediate step 

### How to use:
1. Clone/fork the project
2. Open the project using your favorite SDK (PyCharm, Visual Studio Code, ...)
3. Set the environment variable "OPENAI_API_KEY" to link your OpenAI API Key (https://platform.openai.com/account/api-keys)  
4. Execute the main function from _smarttester\scripts\gtp35_python_smart_testing_example_runner.py_, using the desired function_to_tests and parameters, as follows in this screenshot
![alt text](https://github.com/marcoganassin96/smart-tester/blob/update/readme/assets/gtp35_python_smart_testing_example_runner.png)
5. If parameter "_print_text_" is set as _True_, results are printed in the terminal:
![alt text](https://github.com/marcoganassin96/smart-tester/blob/update/readme/assets/example_generated_code_in_terminal.png)
6. If parameter "_save_text_" is set as _True_, results and intermediate steps are saved as files in __smarttester\package\smarttester\resources\data\saved_files_

### In-progress functionalities:
- Automated post-processing to fix usual LLM's specific errors in generating pytest tests
- Exposition of API to call pytest test generation services from a client

- Develop an LLM-based service to generate test functions for Java, with junit5 (and ParameterizedTest)
- Automated post-processing to fix usual LLM's specific errors in generating junit tests
- Exposition of API to call junit test generation services from a client

- Exposition of a Frontend to provide an interface to the exposed API
  
