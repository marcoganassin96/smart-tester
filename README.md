# Smart Tester

![alt text](https://github.com/marcoganassin96/smart-tester/blob/update/readme/assets/bugs_hunter.png)

A unit test function/classes generator for Python/Java

Provided functionalities
- Develop an LLM based service to generate test functions for Python, with pytest (and pytest.mark.parametrize)
- Saved intermediate steps in persistent files to review step outputs and to restart comuputation from an intermediate step 

In progress functionalities:
- Automated post-processing to fix usual LLM's specific errors in generating pytest tests
- Exposition of API to call pytest test generation services from a client

- Develop an LLM based service to generate test functions for Java, with junit5 (and ParameterizedTest)
- Automated post-processing to fix usual LLM's specific errors in generating junit tests
- Exposition of API to call junit test generation services from a client

- Exposiotion of a Frontend to provide an interface to the exposed API
