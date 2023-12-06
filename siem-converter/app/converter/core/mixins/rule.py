import json
from typing import List

import yaml

from app.converter.core.exceptions.core import InvalidYamlStructure, InvalidJSONStructure
from app.converter.core.mitre import MitreConfig


class JsonRuleMixin:

    def load_rule(self, text):
        try:
            return json.loads(text)
        except json.JSONDecodeError as err:
            raise InvalidJSONStructure(error=str(err))


class YamlRuleMixin:
    mitre_config: MitreConfig = MitreConfig()

    def load_rule(self, text):
        try:
            return yaml.safe_load(text)
        except yaml.YAMLError as err:
            raise InvalidYamlStructure(error=str(err))

    def parse_mitre_attack(self, tags: List[str]) -> dict[str, list]:
        result = {
            'tactics': [],
            'techniques': []
        }
        for tag in tags:
            tag = tag.lower()
            if tag.startswith('attack.'):
                tag = tag[7::]
            if tag.startswith('t'):
                if technique := self.mitre_config.get_technique(tag):
                    result['techniques'].append(technique)
            else:
                if tactic := self.mitre_config.get_tactic(tag):
                    result['tactics'].append(tactic)

        return result
