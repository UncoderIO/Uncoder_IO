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

from app.converter.backends.elasticsearch.const import elasticsearch_lucene_query_details
from app.converter.backends.elasticsearch.mapping import ElasticSearchMappings, elasticsearch_mappings
from app.converter.core.models.platform_details import PlatformDetails
from app.converter.core.render import BaseQueryRender, BaseQueryFieldValue


class ElasticSearchFieldValue(BaseQueryFieldValue):
    details: PlatformDetails = elasticsearch_lucene_query_details

    def apply_value(self, value: Union[str, int]):
        if isinstance(value, int):
            return value
        if " " in value:
            return f'"{value}"'.replace(" ", r"\ ")
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


class ElasticSearchQueryRender(BaseQueryRender):
    details: PlatformDetails = elasticsearch_lucene_query_details
    mappings: ElasticSearchMappings = elasticsearch_mappings

    or_token = "OR"
    and_token = "AND"
    not_token = "NOT"

    field_value_map = ElasticSearchFieldValue(or_token=or_token)
    query_pattern = "{query} {functions}"
    comment_symbol = "//"
    is_multi_line_comment = True

    def generate_prefix(self, logsource: dict) -> str:
        return ""

    def generate_functions(self, functions: list) -> str:
        return ""

