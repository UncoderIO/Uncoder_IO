import json
from typing import Union

import toml
import xmltodict
import yaml

from app.translator.core.exceptions.core import (
    InvalidJSONStructure,
    InvalidTOMLStructure,
    InvalidXMLStructure,
    InvalidYamlStructure,
)
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
                parsed_techniques.append(tag)
            else:
                parsed_tactics.append(tag)
        return self.mitre_config.get_mitre_info(tactics=parsed_tactics, techniques=parsed_techniques)


class XMLRuleMixin:
    @staticmethod
    def load_rule(text: Union[str, bytes]) -> dict:
        try:
            return xmltodict.parse(text)
        except Exception as err:
            raise InvalidXMLStructure(error=str(err)) from err


class TOMLRuleMixin:
    mitre_config: MitreConfig = MitreConfig()

    @staticmethod
    def load_rule(text: str) -> dict:
        try:
            return toml.loads(text)
        except toml.TomlDecodeError as err:
            raise InvalidTOMLStructure(error=str(err)) from err
