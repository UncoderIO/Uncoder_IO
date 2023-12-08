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

from app.translator.core.render import BaseQueryRender
from app.translator.core.render import BaseQueryFieldValue


class LuceneFieldValue(BaseQueryFieldValue):

    def apply_value(self, value: Union[str, int]):
        return value

    def equal_modifier(self, field, value):
        if isinstance(value, list):
            values = self.or_token.join(self.apply_value(f'{v}') for v in value)
            return f"{field}:({values})"
        return f'{field}:{self.apply_value(value)}'

    def contains_modifier(self, field, value):
        if isinstance(value, list):
            values = self.or_token.join(self.apply_value(f'*{v}*') for v in value)
            return f"{field}:({values})"
        prepared_value = self.apply_value(f"*{value}*")
        return f'{field}:{prepared_value}'

    def endswith_modifier(self, field, value):
        if isinstance(value, list):
            values = self.or_token.join(self.apply_value(f'*{v}') for v in value)
            return f"{field}:({values})"
        prepared_value = self.apply_value(f"*{value}")
        return f'{field}:{prepared_value}'

    def startswith_modifier(self, field, value):
        if isinstance(value, list):
            values = self.or_token.join(self.apply_value(f'{v}*') for v in value)
            return f"{field}:({values})"
        prepared_value = self.apply_value(f"{value}*")
        return f'{field}:{prepared_value}'

    def regex_modifier(self, field, value):
        if isinstance(value, list):
            return f"({self.or_token.join(self.regex_modifier(field=field, value=v) for v in value)})"
        return f'{field}:/{value}/'

    def keywords(self, field, value):
        if isinstance(value, list):
            return f"({self.or_token.join(self.keywords(field=field, value=v) for v in value)})"
        return self.apply_value(f"*{value}*")


class LuceneQueryRender(BaseQueryRender):

    or_token = "OR"
    and_token = "AND"
    not_token = "NOT"

    query_pattern = "{query} {functions}"

    comment_symbol = "//"
    is_multi_line_comment = True

    def generate_prefix(self, logsource: dict) -> str:
        return ""
