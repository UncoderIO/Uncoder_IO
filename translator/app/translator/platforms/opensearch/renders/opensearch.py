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
from app.translator.platforms.base.lucene.renders.lucene import LuceneQueryRender, LuceneFieldValue
from app.translator.platforms.opensearch.const import opensearch_query_details
from app.translator.platforms.opensearch.mapping import OpenSearchMappings, opensearch_mappings
from app.translator.core.models.platform_details import PlatformDetails


class OpenSearchFieldValue(LuceneFieldValue):
    details: PlatformDetails = opensearch_query_details

    def equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            values = self.or_token.join(f'"{v}"' for v in value)
            return f"{field}:({values})"
        return f'{field}:"{value}"'

    def less_modifier(self, field: str, value: Union[int, str]) -> str:
        return f'{field}:<"{self.apply_value(value)}"'

    def less_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:
        return f'{field}:[* TO "{self.apply_value(value)}"]'

    def greater_modifier(self, field: str, value: Union[int, str]) -> str:
        return f'{field}:>"{self.apply_value(value)}"'

    def greater_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:
        return f'{field}:["{self.apply_value(value)}" TO *]'

    def not_equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            values = self.or_token.join(self.apply_value(f'"{v}"') for v in value)
            return f"NOT ({field} = ({values})"
        return f'NOT ({field} = "{self.apply_value(value)}")'

    def contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            values = self.or_token.join(f'"*{v}*"' for v in value)
            return f"{field}:({values})"
        return f'{field}:"*{value}*"'

    def endswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            values = self.or_token.join(f'"*{v}"' for v in value)
            return f"{field}:({values})"
        return f'{field}:"*{value}"'

    def startswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            values = self.or_token.join(f'"{v}*"' for v in value)
            return f"{field}:({values})"
        return f'{field}:"{value}*"'

    def regex_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.regex_modifier(field=field, value=v) for v in value)})"
        return f'{field}:/{value}/"'

    def keywords(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.keywords(field=field, value=v) for v in value)})"
        return f'"*{value}*"'


class OpenSearchQueryRender(LuceneQueryRender):
    details: PlatformDetails = opensearch_query_details
    mappings: OpenSearchMappings = opensearch_mappings

    or_token = "OR"
    field_value_map = OpenSearchFieldValue(or_token=or_token)
