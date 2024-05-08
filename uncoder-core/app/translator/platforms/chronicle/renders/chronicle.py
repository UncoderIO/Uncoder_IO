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
from app.translator.core.exceptions.render import UnsupportedRenderMethod
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.render import BaseQueryFieldValue, PlatformQueryRender
from app.translator.platforms.chronicle.const import chronicle_query_details
from app.translator.platforms.chronicle.escape_manager import chronicle_escape_manager
from app.translator.platforms.chronicle.mapping import ChronicleMappings, chronicle_mappings


class ChronicleFieldValue(BaseQueryFieldValue):
    details: PlatformDetails = chronicle_query_details
    escape_manager = chronicle_escape_manager

    def apply_value(self, value: Union[str, int], value_type: str = ValueType.value) -> Union[str, int]:
        if isinstance(value, str):
            if "*" in value:
                return self.apply_asterisk_value(value)
            value = self.clean_str_value(value)
        return super().apply_value(value, value_type)

    def apply_asterisk_value(self, value: str) -> str:
        value = value.replace(r"\\*", "*")
        updated_value = super().apply_value(value, ValueType.regex_value)
        return updated_value.replace(".*", "*").replace("*", ".*")

    @staticmethod
    def clean_str_value(value: str) -> str:
        if value.endswith("/"):
            value = value.rstrip("/")
        return value

    def equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.equal_modifier(field=field, value=v) for v in value)})"
        return f'{field} = "{self.apply_value(value)}" nocase'

    def less_modifier(self, field: str, value: Union[int, str]) -> str:
        return f'{field} < "{self.apply_value(value)}" nocase'

    def less_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:
        return f'{field} <= "{self.apply_value(value)}" nocase'

    def greater_modifier(self, field: str, value: Union[int, str]) -> str:
        return f'{field} > "{self.apply_value(value)}" nocase'

    def greater_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:
        return f'{field} >= "{self.apply_value(value)}" nocase'

    def not_equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.not_equal_modifier(field=field, value=v) for v in value])})"
        return f'{field} != "{self.apply_value(value)}" nocase'

    def contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.contains_modifier(field=field, value=v) for v in value)})"
        return f"{field} = /.*{self.apply_value(value)}.*/ nocase"

    def endswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.endswith_modifier(field=field, value=v) for v in value)})"
        return f"{field} = /.*{self.apply_value(value)}$/ nocase"

    def startswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.startswith_modifier(field=field, value=v) for v in value)})"
        return f"{field} = /^{self.apply_value(value)}.*/ nocase"

    def regex_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.regex_modifier(field=field, value=v) for v in value)})"
        return f"{field} = /{self.apply_asterisk_value(value)}/ nocase"

    def keywords(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        raise UnsupportedRenderMethod(platform_name=self.details.name, method="Keywords")


class ChronicleQueryRender(PlatformQueryRender):
    details: PlatformDetails = chronicle_query_details
    mappings: ChronicleMappings = chronicle_mappings

    is_strict_mapping = True

    or_token = "or"
    and_token = "and"
    not_token = "not"

    field_value_map = ChronicleFieldValue(or_token=or_token)
    query_pattern = "{query} {functions}"
    comment_symbol = "//"
    is_single_line_comment = True
