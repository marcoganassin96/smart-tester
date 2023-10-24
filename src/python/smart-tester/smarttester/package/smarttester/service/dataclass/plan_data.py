from dataclasses import dataclass


@dataclass
class PlanData:
    plan: str = None
    plan_user_message: dict[str, str] = None
    plan_assistant_message: dict[str, str] = None
