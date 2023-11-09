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

from typing import Union, List

from app.converter.backends.qradar.const import qradar_query_details
from app.converter.backends.qradar.mapping import QradarLogSourceSignature, QradarMappings, qradar_mappings
from app.converter.core.models.platform_details import PlatformDetails
from app.converter.core.render import BaseQueryRender, BaseQueryFieldValue


class QradarFieldValue(BaseQueryFieldValue):
    details: PlatformDetails = qradar_query_details

    def equal_modifier(self, field: str, value: Union[Union[int, str, List[int], List[str]]]) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.equal_modifier(field=field, value=v) for v in value])})"
        if field == "UTF8(payload)":
            return f"UTF8(payload) ILIKE '{value}'"
        if isinstance(value, int):
            return f'"{field}"={value}'

        return f'"{field}"=\'{value}\''

    def contains_modifier(self, field, value):
        if isinstance(value, list):
            return f"({self.or_token.join(self.contains_modifier(field=field, value=v) for v in value)})"
        return f'"{field}" ILIKE \'%{value}%\''

    def endswith_modifier(self, field, value):
        if isinstance(value, list):
            return f"({self.or_token.join(self.endswith_modifier(field=field, value=v) for v in value)})"
        return f'"{field}" ILIKE \'%{value}\''

    def startswith_modifier(self, field, value):
        if isinstance(value, list):
            return f"({self.or_token.join(self.startswith_modifier(field=field, value=v) for v in value)})"
        return f'"{field}" ILIKE \'{value}%\''

    def regex_modifier(self, field, value):
        if isinstance(value, list):
            return f"({self.or_token.join(self.regex_modifier(field=field, value=v) for v in value)})"
        return f'"{field}" IMATCHES \'{value}\''

    def keywords(self, field, value):
        if isinstance(value, list):
            return f"({self.or_token.join(self.keywords(field=field, value=v) for v in value)})"
        return f'UTF8(payload) ILIKE "%{value}%"'


class QradarQueryRender(BaseQueryRender):
    details: PlatformDetails = qradar_query_details
    mappings: QradarMappings = qradar_mappings

    or_token = "OR"
    and_token = "AND"
    not_token = "NOT"

    field_value_map = QradarFieldValue(or_token=or_token)
    query_pattern = "{prefix} AND {query} {functions}"

    def generate_prefix(self, log_source_signature: QradarLogSourceSignature) -> str:
        table = str(log_source_signature)
        extra_condition = log_source_signature.extra_condition
        return f"SELECT UTF8(payload) FROM {table} WHERE {extra_condition}"

    def generate_functions(self, functions: list):
        return ""

