import json
from dataclasses import dataclass


@dataclass
class MultiStepData:
    explain_model: str = "gpt-3.5-turbo"
    plan_model: str = "gpt-3.5-turbo"
    execute_model: str = "gpt-3.5-turbo"

    def to_dict(self):
        return {
            "explain_model": self.explain_model,
            "plan_model": self.plan_model,
            "execute_model": self.execute_model,
        }

    def to_json(self):
        return json.dumps(self.to_dict())