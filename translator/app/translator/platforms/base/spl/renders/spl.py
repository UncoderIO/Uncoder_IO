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
from app.translator.core.exceptions.render import UnsupportedRenderMethod
from app.translator.core.render import BaseQueryFieldValue, BaseQueryRender
from app.translator.platforms.base.spl.escape_manager import spl_escape_manager


class SplFieldValue(BaseQueryFieldValue):
    escape_manager = spl_escape_manager

    def equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.equal_modifier(field=field, value=v) for v in value])})"
        return f'{field}="{self.apply_value(value)}"'

    def less_modifier(self, field: str, value: Union[int, str]) -> str:
        return f'{field}<"{self.apply_value(value)}"'

    def less_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:
        return f'{field}<="{self.apply_value(value)}"'

    def greater_modifier(self, field: str, value: Union[int, str]) -> str:
        return f'{field}>"{self.apply_value(value)}"'

    def greater_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:
        return f'{field}>="{self.apply_value(value)}"'

    def not_equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.not_equal_modifier(field=field, value=v) for v in value])})"
        return f'{field}!="{self.apply_value(value)}"'

    def contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.contains_modifier(field=field, value=v) for v in value])})"
        return f'{field}="*{self.apply_value(value)}*"'

    def endswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.endswith_modifier(field=field, value=v) for v in value])})"
        return f'{field}="*{self.apply_value(value)}"'

    def startswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.startswith_modifier(field=field, value=v) for v in value])})"
        return f'{field}="{self.apply_value(value)}*"'

    def keywords(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.keywords(field=field, value=v) for v in value)})"
        return f'"{self.apply_value(value)}"'

    def regex_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        raise UnsupportedRenderMethod(platform_name=self.details.name, method="Regex Expression")


class SplQueryRender(BaseQueryRender):
    or_token = "OR"
    and_token = "AND"
    not_token = "NOT"

    query_pattern = "{prefix} {query} {functions}"
    comment_symbol = "```"

    def wrap_with_comment(self, value: str) -> str:
        return f"{self.comment_symbol} {value} {self.comment_symbol}"
