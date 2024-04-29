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
from app.translator.core.mapping import LogSourceSignature
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.render import BaseQueryFieldValue, PlatformQueryRender
from app.translator.platforms.microsoft.const import microsoft_sentinel_query_details
from app.translator.platforms.microsoft.escape_manager import microsoft_escape_manager
from app.translator.platforms.microsoft.functions import MicrosoftFunctions, microsoft_sentinel_functions
from app.translator.platforms.microsoft.mapping import MicrosoftSentinelMappings, microsoft_sentinel_mappings


class MicrosoftSentinelFieldValue(BaseQueryFieldValue):
    details: PlatformDetails = microsoft_sentinel_query_details
    escape_manager = microsoft_escape_manager

    @staticmethod
    def __escape_value(value: Union[int, str]) -> Union[int, str]:
        return value.replace("'", "''") if isinstance(value, str) else value

    def equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, str):
            return f"{field} =~ @'{self.__escape_value(value)}'"
        if isinstance(value, list):
            prepared_values = ", ".join(f"@'{self.__escape_value(v)}'" for v in value)
            operator = "in~" if all(isinstance(v, str) for v in value) else "in"
            return f"{field} {operator} ({prepared_values})"
        return f"{field} == {self.apply_value(value)}"

    def less_modifier(self, field: str, value: Union[int, str]) -> str:
        if isinstance(value, int):
            return f"{field} < {value}"
        return f"{field} < '{self.apply_value(value)}'"

    def less_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:
        if isinstance(value, int):
            return f"{field} <= {value}"
        return f"{field} <= '{self.apply_value(value)}'"

    def greater_modifier(self, field: str, value: Union[int, str]) -> str:
        if isinstance(value, int):
            return f"{field} > {value}"
        return f"{field} > '{self.apply_value(value)}'"

    def greater_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:
        if isinstance(value, int):
            return f"{field} >= {value}"
        return f"{field} >= '{self.apply_value(value)}'"

    def not_equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.not_equal_modifier(field=field, value=v) for v in value])})"
        if isinstance(value, int):
            return f"{field} !~ {value}"
        return f"{field} !~ '{self.apply_value(value)}'"

    def contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.contains_modifier(field=field, value=v) for v in value)})"
        return f"{field} contains @'{self.__escape_value(value)}'"

    def not_contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.not_contains_modifier(field=field, value=v) for v in value)})"
        return f"{field} !contains @'{self.__escape_value(value)}'"

    def endswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.endswith_modifier(field=field, value=v) for v in value)})"
        return f"{field} endswith @'{self.__escape_value(value)}'"

    def startswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.startswith_modifier(field=field, value=v) for v in value)})"
        return f"{field} startswith @'{self.__escape_value(value)}'"

    def __regex_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        return f"{field} matches regex @'(?i){self.__escape_value(value)}'"

    def regex_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.__regex_modifier(field=field, value=v) for v in value)})"
        return f"({self.__regex_modifier(field=field, value=value)})"

    def not_regex_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"not ({self.or_token.join(self.__regex_modifier(field=field, value=v) for v in value)})"
        return f"not ({self.__regex_modifier(field=field, value=value)})"

    def keywords(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.keywords(field=field, value=v) for v in value)})"
        return f"* contains @'{self.__escape_value(value)}'"

    def is_none(self, field: str, value: Union[str, int]) -> str:
        return f"isempty({self.apply_value(value)})"

    def is_not_none(self, field: str, value: Union[str, int]) -> str:
        return f"isnotempty({self.apply_value(value)})"


class MicrosoftSentinelQueryRender(PlatformQueryRender):
    details: PlatformDetails = microsoft_sentinel_query_details
    platform_functions: MicrosoftFunctions = microsoft_sentinel_functions

    or_token = "or"
    and_token = "and"
    not_token = "not"

    field_value_map = MicrosoftSentinelFieldValue(or_token=or_token)
    query_pattern = "{prefix} | where {query}{functions}"

    mappings: MicrosoftSentinelMappings = microsoft_sentinel_mappings
    comment_symbol = "//"
    is_multi_line_comment = True

    def __init__(self):
        super().__init__()
        self.platform_functions.manager.init_search_func_render(self)

    def generate_prefix(self, log_source_signature: LogSourceSignature) -> str:
        return str(log_source_signature)
