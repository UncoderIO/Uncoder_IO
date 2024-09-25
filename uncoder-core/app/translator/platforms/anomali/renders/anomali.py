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
from app.translator.const import DEFAULT_VALUE_TYPE
from app.translator.core.custom_types.values import ValueType
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.render import BaseFieldValueRender, PlatformQueryRender
from app.translator.managers import render_manager
from app.translator.platforms.anomali.const import anomali_query_details
from app.translator.platforms.anomali.mapping import AnomaliMappings, anomali_query_mappings
from app.translator.platforms.base.sql.str_value_manager import sql_str_value_manager


class AnomaliFieldValueRender(BaseFieldValueRender):
    details: PlatformDetails = anomali_query_details
    str_value_manager = sql_str_value_manager

    @staticmethod
    def _wrap_str_value(value: str) -> str:
        return f"'{value}'"

    def equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.equal_modifier(field=field, value=v) for v in value])})"
        return f"{field} = {self._pre_process_value(field, value, wrap_str=True)}"

    def not_equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.not_equal_modifier(field=field, value=v) for v in value])})"
        return f"{field} != {self._pre_process_value(field, value, wrap_str=True)}"

    def less_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        return f"{field} < {self._pre_process_value(field, value, wrap_str=True)}"

    def less_or_equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        return f"{field} <= {self._pre_process_value(field, value, wrap_str=True)}"

    def greater_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        return f"{field} > {self._pre_process_value(field, value, wrap_str=True)}"

    def greater_or_equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        return f"{field} >= {self._pre_process_value(field, value, wrap_str=True)}"

    def contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.contains_modifier(field=field, value=v) for v in value)})"
        return f"{field} like '%{self._pre_process_value(field, value)}%'"

    def endswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.endswith_modifier(field=field, value=v) for v in value)})"
        return f"{field} like '%{self._pre_process_value(field, value)}'"

    def startswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.startswith_modifier(field=field, value=v) for v in value)})"
        return f"{field} like '{self._pre_process_value(field, value)}%'"

    def regex_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.regex_modifier(field=field, value=v) for v in value)})"
        regex_str = self._pre_process_value(field, value, value_type=ValueType.regex_value, wrap_str=True)
        return f"regexp_like({field}, {regex_str})"

    def keywords(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        return f'message contains "{self._pre_process_value(field, value)}"'


@render_manager.register
class AnomaliQueryRender(PlatformQueryRender):
    details: PlatformDetails = anomali_query_details
    mappings: AnomaliMappings = anomali_query_mappings

    or_token = "OR"
    and_token = "AND"
    not_token = "NOT"

    comment_symbol = "--"
    is_single_line_comment = True

    field_value_render = AnomaliFieldValueRender(or_token=or_token)

    @staticmethod
    def _finalize_search_query(query: str) -> str:
        return f"| where {query}" if query else ""
