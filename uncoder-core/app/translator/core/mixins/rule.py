import json
from typing import Union

import xmltodict
import yaml

from app.translator.core.exceptions.core import InvalidJSONStructure, InvalidXMLStructure, InvalidYamlStructure
from app.translator.core.mitre import MitreConfig, MitreInfoContainer


class JsonRuleMixin:
    mitre_config: MitreConfig = MitreConfig()

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

    def parse_mitre_attack(self, tags: list[str]) -> MitreInfoContainer:
        parsed_techniques = []
        parsed_tactics = []
        for tag in set(tags):
            tag = tag.lower()
            if tag.startswith("attack."):
                tag = tag[7::]
            if tag.startswith("t"):
                if technique := self.mitre_config.get_technique(tag):
                    parsed_techniques.append(technique)
            elif tactic := self.mitre_config.get_tactic(tag):
                parsed_tactics.append(tactic)
        return MitreInfoContainer(tactics=parsed_tactics, techniques=parsed_techniques)


class XMLRuleMixin:
    @staticmethod
    def load_rule(text: Union[str, bytes]) -> dict:
        try:
            return xmltodict.parse(text)
        except Exception as err:
            raise InvalidXMLStructure(error=str(err)) from err
