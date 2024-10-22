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
from app.translator.core.render import BaseFieldValueRender, PlatformQueryRender
from app.translator.managers import render_manager
from app.translator.platforms.microsoft.const import microsoft_sentinel_query_details
from app.translator.platforms.microsoft.custom_types.values import KQLValueType
from app.translator.platforms.microsoft.functions import MicrosoftFunctions, microsoft_sentinel_functions
from app.translator.platforms.microsoft.mapping import MicrosoftSentinelMappings, microsoft_sentinel_query_mappings
from app.translator.platforms.microsoft.str_value_manager import microsoft_kql_str_value_manager


class MicrosoftSentinelFieldValueRender(BaseFieldValueRender):
    details: PlatformDetails = microsoft_sentinel_query_details
    str_value_manager = microsoft_kql_str_value_manager

    @staticmethod
    def _wrap_str_value(value: str, value_type: str = KQLValueType.value) -> str:
        if value_type == KQLValueType.verbatim_single_quotes_regex_value:
            return f"@'(i?){value}'"

        if value_type == KQLValueType.verbatim_double_quotes_regex_value:
            return f'@"(i?){value}"'

        if value_type == KQLValueType.single_quotes_regex_value:
            return f"'{value}'"

        return f"@'{value}'"

    def equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            operator = "in~" if all(isinstance(v, str) for v in value) else "in"
            values = ", ".join(
                self._pre_process_value(field, v, KQLValueType.verbatim_single_quotes_value, wrap_str=True)
                for v in value
            )
            return f"{field} {operator} ({values})"

        operator = "=~" if isinstance(value, str) else "=="
        value = self._pre_process_value(field, value, KQLValueType.verbatim_single_quotes_value, wrap_str=True)
        return f"{field} {operator} {value}"

    def less_modifier(self, field: str, value: Union[int, str]) -> str:
        value = self._pre_process_value(field, value, KQLValueType.verbatim_single_quotes_value, wrap_str=True)
        return f"{field} < {value}"

    def less_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:
        value = self._pre_process_value(field, value, KQLValueType.verbatim_single_quotes_value, wrap_str=True)
        return f"{field} <= {value}"

    def greater_modifier(self, field: str, value: Union[int, str]) -> str:
        value = self._pre_process_value(field, value, KQLValueType.verbatim_single_quotes_value, wrap_str=True)
        return f"{field} > {value}"

    def greater_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:
        value = self._pre_process_value(field, value, KQLValueType.verbatim_single_quotes_value, wrap_str=True)
        return f"{field} >= {value}"

    def not_equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.not_equal_modifier(field=field, value=v) for v in value])})"

        operator = "!~" if isinstance(value, str) else "!="
        value = self._pre_process_value(field, value, KQLValueType.verbatim_single_quotes_value, wrap_str=True)
        return f"{field} {operator} {value}"

    def contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.contains_modifier(field=field, value=v) for v in value)})"

        value = self._pre_process_value(field, value, KQLValueType.verbatim_single_quotes_value, wrap_str=True)
        return f"{field} contains {value}"

    def not_contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.not_contains_modifier(field=field, value=v) for v in value)})"

        value = self._pre_process_value(field, value, KQLValueType.verbatim_single_quotes_value, wrap_str=True)
        return f"{field} !contains {value}"

    def endswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.endswith_modifier(field=field, value=v) for v in value)})"

        value = self._pre_process_value(field, value, KQLValueType.verbatim_single_quotes_value, wrap_str=True)
        return f"{field} endswith {value}"

    def startswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.startswith_modifier(field=field, value=v) for v in value)})"

        value = self._pre_process_value(field, value, KQLValueType.verbatim_single_quotes_value, wrap_str=True)
        return f"{field} startswith {value}"

    @staticmethod
    def __get_regex_value_type(value: DEFAULT_VALUE_TYPE) -> str:
        has_single_quote = "'" in value
        has_double_quote = '"' in value
        if has_single_quote:
            if has_double_quote:
                return KQLValueType.single_quotes_regex_value
            return KQLValueType.verbatim_double_quotes_regex_value
        return KQLValueType.verbatim_single_quotes_regex_value

    def __regex_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        value_type = self.__get_regex_value_type(value)
        return f"{field} matches regex {self._pre_process_value(field, value, value_type, wrap_str=True)}"

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

        value = self._pre_process_value(field, value, KQLValueType.verbatim_single_quotes_value, wrap_str=True)
        return f"* contains {value}"

    def is_none(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.is_none(field=field, value=v) for v in value)})"

        return f"isempty({field})"

    def is_not_none(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.is_not_none(field=field, value=v) for v in value)})"

        return f"isnotempty({field})"


@render_manager.register
class MicrosoftSentinelQueryRender(PlatformQueryRender):
    details: PlatformDetails = microsoft_sentinel_query_details
    platform_functions: MicrosoftFunctions = None

    or_token = "or"
    and_token = "and"
    not_token = "not"

    field_value_render = MicrosoftSentinelFieldValueRender(or_token=or_token)

    mappings: MicrosoftSentinelMappings = microsoft_sentinel_query_mappings
    comment_symbol = "//"
    is_single_line_comment = True

    def init_platform_functions(self) -> None:
        self.platform_functions = microsoft_sentinel_functions
        self.platform_functions.platform_query_render = self

    def generate_prefix(self, log_source_signature: LogSourceSignature, functions_prefix: str = "") -> str:  # noqa: ARG002
        return str(log_source_signature)

    @staticmethod
    def _finalize_search_query(query: str) -> str:
        return f"| where {query}" if query else ""
