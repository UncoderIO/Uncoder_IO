"""
Uncoder IO Community Edition License
-----------------------------------------------------------------
Copyright (c) 2024 SOC Prime, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-----------------------------------------------------------------
"""

from typing import Union

from app.translator.const import DEFAULT_VALUE_TYPE
from app.translator.core.custom_types.values import ValueType
from app.translator.core.mapping import SourceMapping
from app.translator.core.models.functions.base import Function
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.render import BaseQueryFieldValue, PlatformQueryRender
from app.translator.platforms.qradar.const import qradar_query_details
from app.translator.platforms.qradar.escape_manager import qradar_escape_manager
from app.translator.platforms.qradar.mapping import QradarLogSourceSignature, QradarMappings, qradar_mappings


class QradarFieldValue(BaseQueryFieldValue):
    details: PlatformDetails = qradar_query_details
    escape_manager = qradar_escape_manager

    def apply_value(self, value: Union[str, int], value_type: str = ValueType.value) -> Union[str, int]:  # noqa: ARG002
        if isinstance(value, str):
            value = value.replace("_", "__").replace("%", "%%").replace("\\'", "%").replace("'", '"')
            if value.endswith("\\\\%"):
                value = value.replace("\\\\%", "\\%")
        return value

    def _apply_value(self, value: Union[str, int]) -> Union[str, int]:
        if isinstance(value, str) and "\\" in value:
            return value
        return self.apply_value(value)

    def equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.equal_modifier(field=field, value=v) for v in value])})"
        if field == "UTF8(payload)":
            return f"UTF8(payload) ILIKE '{self.apply_value(value)}'"
        if isinstance(value, int):
            return f'"{field}"={value}'

        return f"\"{field}\"='{self._apply_value(value)}'"

    def less_modifier(self, field: str, value: Union[int, str]) -> str:
        if isinstance(value, int):
            return f'"{field}"<{value}'
        return f"\"{field}\"<'{self._apply_value(value)}'"

    def less_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:
        if isinstance(value, int):
            return f'"{field}"<={value}'
        return f"\"{field}\"<='{self._apply_value(value)}'"

    def greater_modifier(self, field: str, value: Union[int, str]) -> str:
        if isinstance(value, int):
            return f'"{field}">{value}'
        return f"\"{field}\">'{self._apply_value(value)}'"

    def greater_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:
        if isinstance(value, int):
            return f'"{field}">={value}'
        return f"\"{field}\">='{self._apply_value(value)}'"

    def not_equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.not_equal_modifier(field=field, value=v) for v in value])})"
        if isinstance(value, int):
            return f'"{field}"!={value}'
        return f"\"{field}\"!='{self._apply_value(value)}'"

    def contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.contains_modifier(field=field, value=v) for v in value)})"
        return f"\"{field}\" ILIKE '%{self._apply_value(value)}%'"

    def endswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.endswith_modifier(field=field, value=v) for v in value)})"
        return f"\"{field}\" ILIKE '%{self._apply_value(value)}'"

    def startswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.startswith_modifier(field=field, value=v) for v in value)})"
        return f"\"{field}\" ILIKE '{self._apply_value(value)}%'"

    def regex_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.regex_modifier(field=field, value=v) for v in value)})"
        return f"\"{field}\" IMATCHES '{value}'"

    def keywords(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.keywords(field=field, value=v) for v in value)})"
        return f"UTF8(payload) ILIKE '%{self.apply_value(value)}%'"


class QradarQueryRender(PlatformQueryRender):
    details: PlatformDetails = qradar_query_details
    mappings: QradarMappings = qradar_mappings

    or_token = "OR"
    and_token = "AND"
    not_token = "NOT"

    field_value_map = QradarFieldValue(or_token=or_token)
    query_pattern = "{prefix} AND {query} {functions}"

    def generate_prefix(self, log_source_signature: QradarLogSourceSignature) -> str:
        table = str(log_source_signature)
        extra_condition = log_source_signature.extra_condition
        return f"SELECT UTF8(payload) FROM {table} WHERE {extra_condition}"

    def wrap_with_comment(self, value: str) -> str:
        return f"/* {value} */"

    def generate_functions(self, functions: list[Function], source_mapping: SourceMapping) -> str:  # noqa: ARG002
        return ""
