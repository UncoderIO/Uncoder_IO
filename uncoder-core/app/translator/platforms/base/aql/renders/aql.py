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
from app.translator.core.render import BaseQueryFieldValue, PlatformQueryRender
from app.translator.core.str_value_manager import StrValue
from app.translator.platforms.base.aql.mapping import AQLLogSourceSignature, AQLMappings, aql_mappings
from app.translator.platforms.base.aql.str_value_manager import aql_str_value_manager


class AQLFieldValue(BaseQueryFieldValue):
    str_value_manager = aql_str_value_manager

    @staticmethod
    def _wrap_str_value(value: str) -> str:
        return f"'{value}'"

    def equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.equal_modifier(field=field, value=v) for v in value])})"
        if isinstance(value, StrValue) and value.has_spec_symbols:
            return self.__render_i_like(field, value)
        return f'"{field}"={self._pre_process_value(field, value, value_type=ValueType.value, wrap_str=True)}'

    def less_modifier(self, field: str, value: Union[int, str, StrValue]) -> str:
        return f'"{field}"<{self._pre_process_value(field, value, value_type=ValueType.value, wrap_str=True)}'

    def less_or_equal_modifier(self, field: str, value: Union[int, str, StrValue]) -> str:
        return f'"{field}"<={self._pre_process_value(field, value, value_type=ValueType.value, wrap_str=True)}'

    def greater_modifier(self, field: str, value: Union[int, str, StrValue]) -> str:
        return f'"{field}">{self._pre_process_value(field, value, value_type=ValueType.value, wrap_str=True)}'

    def greater_or_equal_modifier(self, field: str, value: Union[int, str, StrValue]) -> str:
        return f'"{field}">={self._pre_process_value(field, value, value_type=ValueType.value, wrap_str=True)}'

    def not_equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.not_equal_modifier(field=field, value=v) for v in value])})"
        if isinstance(value, StrValue) and value.has_spec_symbols:
            return self.__render_i_like(field, value, not_=True)
        return f'"{field}"!={self._pre_process_value(field, value, value_type=ValueType.value, wrap_str=True)}'

    def contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.contains_modifier(field=field, value=v) for v in value)})"
        return self.__render_i_like(field, value, startswith=True, endswith=True)

    def endswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.endswith_modifier(field=field, value=v) for v in value)})"
        return self.__render_i_like(field, value, endswith=True)

    def startswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.startswith_modifier(field=field, value=v) for v in value)})"
        return self.__render_i_like(field, value, startswith=True)

    def __render_i_like(
        self,
        field: str,
        value: DEFAULT_VALUE_TYPE,
        startswith: bool = False,
        endswith: bool = False,
        not_: bool = False,
    ) -> str:
        prefix = "%" if endswith else ""
        re_prefix = ".*" if endswith else ""
        suffix = "%" if startswith else ""
        re_suffix = ".*" if startswith else ""
        if self.__has_special_symbols(value):
            re_value = self._pre_process_value(field, value, value_type=ValueType.regex_value)
            return self.__regex_modifier(field, f"{re_prefix}{re_value}{re_suffix}")

        value = self._pre_process_value(field, value, value_type=ValueType.value)
        not_ = "NOT " if not_ else ""
        return f"\"{field}\" {not_}ILIKE '{prefix}{value}{suffix}'"

    @staticmethod
    def __has_special_symbols(value: DEFAULT_VALUE_TYPE) -> bool:
        if any(char for char in str(value) if char in ("%", "_")):
            return True

        return False

    @staticmethod
    def __regex_modifier(field: str, value: str) -> str:
        return f"\"{field}\" IMATCHES '{value}'"

    def regex_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.regex_modifier(field=field, value=v) for v in value)})"

        if isinstance(value, StrValue):
            value = self.str_value_manager.from_container_to_str(value, value_type=ValueType.regex_value)
        return self.__regex_modifier(field, value)

    def keywords(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.keywords(field=field, value=v) for v in value)})"
        return self.__render_i_like("UTF8(payload)", value, startswith=True, endswith=True)


class AQLQueryRender(PlatformQueryRender):
    mappings: AQLMappings = aql_mappings

    or_token = "OR"
    and_token = "AND"
    not_token = "NOT"

    field_value_map = AQLFieldValue(or_token=or_token)

    def generate_prefix(self, log_source_signature: AQLLogSourceSignature, functions_prefix: str = "") -> str:  # noqa: ARG002
        table = str(log_source_signature)
        extra_condition = log_source_signature.extra_condition
        return f"SELECT UTF8(payload) FROM {table} WHERE {extra_condition}"

    def wrap_with_comment(self, value: str) -> str:
        return f"/* {value} */"

    @staticmethod
    def _finalize_search_query(query: str) -> str:
        return f"AND {query}" if query else ""
