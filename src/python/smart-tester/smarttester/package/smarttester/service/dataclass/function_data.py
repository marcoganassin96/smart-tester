from dataclasses import dataclass


@dataclass
class FunctionData:
    function: str = None
    programming_language: str = "python"
    unit_test_package: str = "pytest"
