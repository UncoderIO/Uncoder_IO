"""
Uncoder IO Community Edition License
-----------------------------------------------------------------
Copyright (c) 2023 SOC Prime, Inc.

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
from app.translator.core.render import BaseQueryFieldValue, BaseQueryRender
from app.translator.core.str_value_manager import StrValue
from app.translator.platforms.base.lucene.mapping import LuceneLogSourceSignature
from app.translator.platforms.base.lucene.str_value_manager import lucene_str_value_manager


class LuceneFieldValue(BaseQueryFieldValue):
    str_value_manager = lucene_str_value_manager

    @staticmethod
    def __get_value_type(field_name: str, value_type: str = ValueType.value) -> str:
        is_ip_field = field_name and (field_name.endswith(".ip") or field_name.endswith(".address"))
        if is_ip_field and value_type != ValueType.regex_value:
            return ValueType.ip

        return ValueType.value

    def _pre_process_values_list(
        self, field: str, values: list[Union[int, str, StrValue]], value_type: str = ValueType.value
    ) -> list[str]:
        value_type = self.__get_value_type(field, value_type)
        processed = []
        for v in values:
            if isinstance(v, StrValue):
                processed.append(self.str_value_manager.from_container_to_str(v, value_type))
            elif isinstance(v, str):
                processed.append(self.str_value_manager.escape_manager.escape(v, value_type))
            else:
                processed.append(str(v))
        return processed

    def _pre_process_value(
        self, field: str, value: Union[int, str, StrValue], value_type: str = ValueType.value
    ) -> Union[int, str]:
        value_type = self.__get_value_type(field, value_type)
        if isinstance(value, StrValue):
            return self.str_value_manager.from_container_to_str(value, value_type)
        if isinstance(value, str):
            return self.str_value_manager.escape_manager.escape(value, value_type)
        return value

    def equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            values = self.or_token.join(self._pre_process_values_list(field, value))
            return f"{field}:({values})"
        return f"{field}:{self._pre_process_value(field, value)}"

    def less_modifier(self, field: str, value: Union[int, str, StrValue]) -> str:
        return f"{field}:<{self._pre_process_value(field, value)}"

    def less_or_equal_modifier(self, field: str, value: Union[int, str, StrValue]) -> str:
        return f"{field}:[* TO {self._pre_process_value(field, value)}]"

    def greater_modifier(self, field: str, value: Union[int, str, StrValue]) -> str:
        return f"{field}:>{self._pre_process_value(field, value)}"

    def greater_or_equal_modifier(self, field: str, value: Union[int, str, StrValue]) -> str:
        return f"{field}:[{self._pre_process_value(field, value)} TO *]"

    def not_equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            values = self.or_token.join(self._pre_process_values_list(field, value))
            return f"NOT ({field} = ({values})"
        return f"NOT ({field} = {self._pre_process_value(field, value)})"

    def contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            values = self.or_token.join(f"*{v}*" for v in self._pre_process_values_list(field, value))
            return f"{field}:({values})"
        return f"{field}:*{self._pre_process_value(field, value)}*"

    def endswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            values = self.or_token.join(f"*{v}" for v in self._pre_process_values_list(field, value))
            return f"{field}:({values})"
        return f"{field}:*{self._pre_process_value(field, value)}"

    def startswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            values = self.or_token.join(f"{v}*" for v in self._pre_process_values_list(field, value))
            return f"{field}:({values})"
        return f"{field}:{self._pre_process_value(field, value)}*"

    def regex_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.regex_modifier(field=field, value=v) for v in value)})"

        if isinstance(value, StrValue):
            return f"{field}:/{self._pre_process_value(field, value, value_type=ValueType.regex_value)}/"

        return f"{field}:/{value}/"

    def keywords(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.keywords(field=field, value=v) for v in value)})"
        return f"*{self._pre_process_value(field, value)}*"


class LuceneQueryRender(BaseQueryRender):
    or_token = "OR"
    and_token = "AND"
    not_token = "NOT"

    query_pattern = "{query} {functions}"

    comment_symbol = "//"
    is_multi_line_comment = True

    def generate_prefix(self, log_source_signature: LuceneLogSourceSignature) -> str:  # noqa: ARG002
        return ""
