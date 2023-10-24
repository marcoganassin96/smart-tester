from dataclasses import dataclass


@dataclass
class ExplainData:
    explanation: str = None
    explain_system_message: dict[str, str] = None
    explain_user_message: dict[str, str] = None
    explain_assistant_message: dict[str, str] = None
