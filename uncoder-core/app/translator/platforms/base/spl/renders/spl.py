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
from app.translator.core.render import BaseFieldValueRender, PlatformQueryRender
from app.translator.core.str_value_manager import StrValue
from app.translator.platforms.base.spl.str_value_manager import spl_str_value_manager


class SplFieldValueRender(BaseFieldValueRender):
    str_value_manager = spl_str_value_manager

    @staticmethod
    def _wrap_str_value(value: str) -> str:
        return f'"{value}"'

    def _pre_process_value(
        self, field: str, value: Union[int, str, StrValue], value_type: str = ValueType.value, wrap_str: bool = False
    ) -> Union[int, str]:
        value = super()._pre_process_value(field, value, value_type=value_type, wrap_str=wrap_str)
        return self._wrap_str_value(str(value)) if not isinstance(value, str) else value

    def equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.equal_modifier(field=field, value=v) for v in value])})"
        return f"{field}={self._pre_process_value(field, value, wrap_str=True)}"

    def less_modifier(self, field: str, value: Union[int, str]) -> str:
        return f"{field}<{self._pre_process_value(field, value, wrap_str=True)}"

    def less_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:
        return f"{field}<={self._pre_process_value(field, value, wrap_str=True)}"

    def greater_modifier(self, field: str, value: Union[int, str]) -> str:
        return f"{field}>{self._pre_process_value(field, value, wrap_str=True)}"

    def greater_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:
        return f"{field}>={self._pre_process_value(field, value, wrap_str=True)}"

    def not_equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.not_equal_modifier(field=field, value=v) for v in value])})"
        return f"{field}!={self._pre_process_value(field, value, wrap_str=True)}"

    def contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.contains_modifier(field=field, value=v) for v in value])})"
        return f'{field}="*{self._pre_process_value(field, value)}*"'

    def endswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.endswith_modifier(field=field, value=v) for v in value])})"
        return f'{field}="*{self._pre_process_value(field, value)}"'

    def startswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.startswith_modifier(field=field, value=v) for v in value])})"
        return f'{field}="{self._pre_process_value(field, value)}*"'

    def keywords(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.keywords(field=field, value=v) for v in value)})"
        return f"{self._pre_process_value(field, value, wrap_str=True)}"

    def regex_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        raise UnsupportedRenderMethod(platform_name=self.details.name, method="Regex Expression")


class SplQueryRender(PlatformQueryRender):
    or_token = "OR"
    and_token = "AND"
    not_token = "NOT"

    comment_symbol = "```"

    def wrap_with_comment(self, value: str) -> str:
        return f"{self.comment_symbol} {value} {self.comment_symbol}"
