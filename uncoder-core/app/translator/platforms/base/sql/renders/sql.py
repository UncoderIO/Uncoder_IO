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
from app.translator.core.exceptions.render import UnsupportedRenderMethod
from app.translator.core.mapping import LogSourceSignature
from app.translator.core.render import BaseQueryFieldValue, PlatformQueryRender


class SqlFieldValue(BaseQueryFieldValue):
    def equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.equal_modifier(field=field, value=v) for v in value])})"
        return f"{field} = '{value}'"

    def less_modifier(self, field: str, value: Union[int, str]) -> str:
        return f"{field} < '{value}'"

    def less_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:
        return f"{field} <= '{value}'"

    def greater_modifier(self, field: str, value: Union[int, str]) -> str:
        return f"{field} > '{value}'"

    def greater_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:
        return f"{field} >= '{value}'"

    def not_equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.not_equal_modifier(field=field, value=v) for v in value])})"
        return f"{field} != '{value}'"

    def contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.contains_modifier(field=field, value=v) for v in value)})"
        return f"{field} ILIKE '%{value}%'  ESCAPE '\\'"

    def endswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.endswith_modifier(field=field, value=v) for v in value)})"
        return f"{field} ILIKE '%{value}'  ESCAPE '\\'"

    def startswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.startswith_modifier(field=field, value=v) for v in value)})"
        return f"{field} ILIKE '{value}%'  ESCAPE '\\'"

    def regex_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.regex_modifier(field=field, value=v) for v in value)})"
        return f"{field} ILIKE '{value}'  ESCAPE '\\'"

    def keywords(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        raise UnsupportedRenderMethod(platform_name=self.details.name, method="Keywords")


class SqlQueryRender(PlatformQueryRender):
    or_token = "OR"
    and_token = "AND"
    not_token = "NOT"

    comment_symbol = "--"
    is_single_line_comment = True

    def generate_prefix(self, log_source_signature: LogSourceSignature, functions_prefix: str = "") -> str:  # noqa: ARG002
        table = str(log_source_signature) if str(log_source_signature) else "eventlog"
        return f"SELECT * FROM {table}"

    @staticmethod
    def _finalize_search_query(query: str) -> str:
        return f"WHERE {query}" if query else ""
