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
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.managers import render_manager
from app.translator.core.render import BaseQueryFieldValue, PlatformQueryRender

from app.translator.platforms.sumo_logic.const import sumologic_search_query_details
from app.translator.platforms.sumo_logic.mapping import SumoLogicMappings, sumologic_mappings


class SumologicFieldValue(BaseQueryFieldValue):
    details: PlatformDetails = sumologic_search_query_details

    def equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.equal_modifier(field=field, value=v) for v in value])})"
        if isinstance(value, str) and " " in value:
            return f'{field}="{value}"'
        return f'{field}="{value}"'

    def less_modifier(self, field: str, value: Union[int, str]) -> str:
        if isinstance(value, str) and " " in value:
            return f'{field}<"{value}"'
        return f'{field}<{value}'

    def less_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:
        if isinstance(value, str) and " " in value:
            return f'{field}<="{value}"'
        return f'{field}<={value}'

    def greater_modifier(self, field: str, value: Union[int, str]) -> str:
        if isinstance(value, str) and " " in value:
            return f'{field}>"{value}"'
        return f'{field}>{value}'

    def greater_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:
        if isinstance(value, str) and " " in value:
            return f'{field}>="{value}"'
        return f'{field}>={value}'

    def not_equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.not_equal_modifier(field=field, value=v) for v in value])})"
        if isinstance(value, str) and " " in value:
            return f'{field}!="{value}"'
        return f'{field}!={value}'

    def contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return self.or_token.join([self.contains_modifier(field=field, value=v) for v in value])
        return f'{field}=*"{value}"*'

    def endswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return self.or_token.join([self.endswith_modifier(field=field, value=v) for v in value])
        return f'{field}=*"{value}"'

    def startswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return self.or_token.join([self.startswith_modifier(field=field, value=v) for v in value])
        return f'{field}="{value}"*'

    def keywords(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.keywords(field=field, value=v) for v in value)})"
        return f'"{value}"'


@render_manager.register
class SumologicSearchQueryRender(PlatformQueryRender):
    details: PlatformDetails = sumologic_search_query_details
    mappings: SumoLogicMappings = sumologic_mappings

    or_token = "OR"
    and_token = "AND"
    not_token = "NOT"

    field_value_map = SumologicFieldValue(or_token=or_token)
    query_pattern = "{prefix} {query} {functions}"