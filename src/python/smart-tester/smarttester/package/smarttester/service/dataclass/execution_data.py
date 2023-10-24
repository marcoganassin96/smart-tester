from dataclasses import dataclass


@dataclass
class ExecutionData:
    execution: str = None
    execute_system_message: dict[str, str] = None
    execute_user_message: dict[str, str] = None
