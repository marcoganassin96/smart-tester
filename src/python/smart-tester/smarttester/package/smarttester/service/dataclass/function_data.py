from dataclasses import dataclass


@dataclass
class FunctionData:
    function: str = None
    function_name: str = "Unknown"
    programming_language: str = "python"
    unit_test_package: str = "pytest"
