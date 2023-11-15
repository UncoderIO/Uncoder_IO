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

from app.converter.backends.opensearch.const import opensearch_query_details
from app.converter.backends.opensearch.mapping import OpenSearchMappings, opensearch_mappings
from app.converter.core.models.platform_details import PlatformDetails
from app.converter.core.render import BaseQueryRender, BaseQueryFieldValue


class OpenSearchFieldValue(BaseQueryFieldValue):
    details: PlatformDetails = opensearch_query_details

    def equal_modifier(self, field, value):
        if isinstance(value, list):
            values = self.or_token.join(f'"{v}"' for v in value)
            return f"{field}:({values})"
        return f'{field}:"{value}"'

    def contains_modifier(self, field, value):
        if isinstance(value, list):
            values = self.or_token.join(f'"*{v}*"' for v in value)
            return f"{field}:({values})"
        return f'{field}:"*{value}*"'

    def endswith_modifier(self, field, value):
        if isinstance(value, list):
            values = self.or_token.join(f'"*{v}"' for v in value)
            return f"{field}:({values})"
        return f'{field}:"*{value}"'

    def startswith_modifier(self, field, value):
        if isinstance(value, list):
            values = self.or_token.join(f'"{v}*"' for v in value)
            return f"{field}:({values})"
        return f'{field}:"{value}*"'

    def regex_modifier(self, field, value):
        if isinstance(value, list):
            return f"({self.or_token.join(self.regex_modifier(field=field, value=v) for v in value)})"
        return f'{field}:/{value}/"'

    def keywords(self, field, value):
        if isinstance(value, list):
            return f"({self.or_token.join(self.keywords(field=field, value=v) for v in value)})"
        return f'"*{value}*"'


class OpenSearchQueryRender(BaseQueryRender):
    details: PlatformDetails = opensearch_query_details
    mappings: OpenSearchMappings = opensearch_mappings

    or_token = "OR"
    and_token = "AND"
    not_token = "NOT"

    field_value_map = OpenSearchFieldValue(or_token=or_token)
    query_pattern = "{query} {functions}"
    comment_symbol = "//"
    is_multi_line_comment = True

    def generate_prefix(self, logsource: dict) -> str:
        return ""

    def generate_functions(self, functions: list) -> str:
        return ""

