import json

import yaml

from app.converter.core.exceptions.core import InvalidYamlStructure, InvalidJSONStructure


class JsonRuleMixin:

    def load_rule(self, text):
        try:
            return json.loads(text)
        except json.JSONDecodeError as err:
            raise InvalidJSONStructure(error=str(err))


class YamlRuleMixin:

    def load_rule(self, text):
        try:
            return yaml.safe_load(text)
        except yaml.YAMLError as err:
            raise InvalidYamlStructure(error=str(err))
