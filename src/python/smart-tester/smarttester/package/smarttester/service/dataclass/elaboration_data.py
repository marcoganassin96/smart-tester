from dataclasses import dataclass


@dataclass
class ElaborationData:
    elaboration: str = None
    elaboration_needed: bool = False
    elaboration_user_message: dict[str, str] = None
    elaboration_assistant_message: dict[str, str] = None
