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
from typing import Optional, Union

from app.translator.const import DEFAULT_VALUE_TYPE
from app.translator.core.custom_types.values import ValueType
from app.translator.core.exceptions.render import UnsupportedRenderMethod
from app.translator.core.mapping import LogSourceSignature
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.render import BaseFieldValueRender, PlatformQueryRender
from app.translator.managers import render_manager
from app.translator.platforms.elasticsearch.const import elasticsearch_esql_query_details
from app.translator.platforms.elasticsearch.mapping import ElasticESQLMappings, esql_query_mappings
from app.translator.platforms.elasticsearch.str_value_manager import (
    ESQLStrValueManager,
    esql_str_value_manager
)


class ESQLFieldValueRender(BaseFieldValueRender):
    details: PlatformDetails = elasticsearch_esql_query_details
    str_value_manager: ESQLStrValueManager = esql_str_value_manager

    @staticmethod
    def _make_case_insensitive(value: str) -> str:
        container: list[str] = []
        for v in value:
            if v.isalpha():
                container.append(f"[{v.upper()}{v.lower()}]")
            else:
                container.append(v)
        return "".join(container)

    @staticmethod
    def _wrap_str_value(value: str) -> str:
        return f'"{value}"'

    @staticmethod
    def _wrap_int_value(value: int) -> str:
        return f'"{value}"'

    def equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.equal_modifier(field=field, value=v) for v in value])})"
        value = self._pre_process_value(field, value, value_type=ValueType.value, wrap_str=True, wrap_int=True)
        return f"{field} == {value}"

    def less_modifier(self, field: str, value: Union[int, str]) -> str:
        value = self._pre_process_value(field, value, value_type=ValueType.value, wrap_str=True, wrap_int=True)
        return f"{field} < {value}"

    def less_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:
        value = self._pre_process_value(field, value, value_type=ValueType.value, wrap_str=True, wrap_int=True)
        return f"{field} <= {value}"

    def greater_modifier(self, field: str, value: Union[int, str]) -> str:
        value = self._pre_process_value(field, value, value_type=ValueType.value, wrap_str=True, wrap_int=True)
        return f"{field} > {value}"

    def greater_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:
        value = self._pre_process_value(field, value, value_type=ValueType.value, wrap_str=True, wrap_int=True)
        return f"{field} >= {value}"

    def not_equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.not_equal_modifier(field=field, value=v) for v in value])})"
        value = self._pre_process_value(field, value, value_type=ValueType.value, wrap_str=True, wrap_int=True)
        return f"{field} != {value}"

    def contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.contains_modifier(field=field, value=v) for v in value)})"
        if field.endswith(".text"):
            return self.regex_modifier(field=field, value=value)
        value = self._pre_process_value(field, value, value_type=ValueType.value, wrap_str=False, wrap_int=True)
        return f'{field} like "*{value}*"'

    def endswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if field.endswith(".text"):
            return self.regex_modifier(field=field, value=value)
        if isinstance(value, list):
            return f"({self.or_token.join(self.endswith_modifier(field=field, value=v) for v in value)})"
        value = self._pre_process_value(field, value, value_type=ValueType.value, wrap_str=True, wrap_int=True)
        return f"ends_with({field}, {value})"

    def startswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if field.endswith(".text"):
            return self.regex_modifier(field=field, value=value)
        if isinstance(value, list):
            return f"({self.or_token.join(self.startswith_modifier(field=field, value=v) for v in value)})"
        value = self._pre_process_value(field, value, value_type=ValueType.value, wrap_str=True, wrap_int=True)
        return f"starts_with({field}, {value})"

    def regex_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.regex_modifier(field=field, value=v) for v in value)})"
        value = self._pre_process_value(field, value, value_type=ValueType.regex_value, wrap_str=False, wrap_int=True)
        if isinstance(value, str):
            value = self._make_case_insensitive(value)
        return f'{field} rlike ".*{value}.*"'

    def keywords(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        raise UnsupportedRenderMethod(platform_name=self.details.name, method="Keywords")


@render_manager.register
class ESQLQueryRender(PlatformQueryRender):
    details: PlatformDetails = elasticsearch_esql_query_details
    mappings: ElasticESQLMappings = esql_query_mappings
    comment_symbol = "//"

    or_token = "or"
    and_token = "and"
    not_token = "not"
    field_value_render = ESQLFieldValueRender(or_token=or_token)

    def generate_prefix(self, log_source_signature: Optional[LogSourceSignature], functions_prefix: str = "") -> str:  # noqa: ARG002
        table = str(log_source_signature) if str(log_source_signature) else "*"
        return f"FROM {table} |"

    @staticmethod
    def _finalize_search_query(query: str) -> str:
        return f"WHERE {query}" if query else ""
