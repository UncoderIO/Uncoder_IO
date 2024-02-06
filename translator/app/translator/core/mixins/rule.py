import json

import yaml

from app.translator.core.exceptions.core import InvalidJSONStructure, InvalidYamlStructure
from app.translator.core.mitre import MitreConfig


class JsonRuleMixin:
    @staticmethod
    def load_rule(text: str) -> dict:
        try:
            return json.loads(text)
        except json.JSONDecodeError as err:
            raise InvalidJSONStructure(error=str(err)) from err


class YamlRuleMixin:
    mitre_config: MitreConfig = MitreConfig()

    @staticmethod
    def load_rule(text: str) -> dict:
        try:
            return yaml.safe_load(text)
        except yaml.YAMLError as err:
            raise InvalidYamlStructure(error=str(err)) from err

    def parse_mitre_attack(self, tags: list[str]) -> dict[str, list]:
        result = {"tactics": [], "techniques": []}
        for tag in set(tags):
            tag = tag.lower()
            if tag.startswith("attack."):
                tag = tag[7::]
            if tag.startswith("t"):
                if technique := self.mitre_config.get_technique(tag):
                    result["techniques"].append(technique)
            elif tactic := self.mitre_config.get_tactic(tag):
                result["tactics"].append(tactic)

        return result
