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
from typing import List, Union

from app.translator.core.custom_types.tokens import LogicalOperatorType, GroupType
from app.translator.core.models.field import Field, Keyword
from app.translator.platforms.sumo_logic.const import sumologic_query_details
from app.translator.core.mapping import SourceMapping, BasePlatformMappings, LogSourceSignature
from app.translator.core.models.functions.base import Function
from app.translator.const import DEFAULT_VALUE_TYPE
from app.translator.core.render import BaseQueryRender, BaseQueryFieldValue
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.platforms.sumo_logic.mapping import sumologic_mappings


class SumoLogicFieldValue(BaseQueryFieldValue):
    details: PlatformDetails = sumologic_query_details

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


class SumoLogicQueryRender(BaseQueryRender):
    details: PlatformDetails = sumologic_query_details
    mappings: BasePlatformMappings = sumologic_mappings

    or_token = "OR"
    and_token = "AND"
    not_token = "NOT"

    field_value_map = SumoLogicFieldValue(or_token=or_token)
    query_pattern = "{prefix} AND {query} {functions}"

    def generate_prefix(self, log_source_signature: LogSourceSignature) -> str:
        if str(log_source_signature):
            return str(log_source_signature)
        return ""

    def generate_functions(self, functions: List[Function], source_mapping: SourceMapping) -> str:
        return ""

    def map_field(self, field: Field, source_mapping: SourceMapping) -> Union[List[str], list[None]]:
        generic_field_name = field.generic_names_map[source_mapping.source_id]
        # field can be mapped to corresponding platform field name or list of platform field names
        mapped_field = source_mapping.fields_mapping.get_platform_field_name(generic_field_name=generic_field_name)
        if not mapped_field:
            return [None]

        if isinstance(mapped_field, str):
            mapped_field = [mapped_field]

        return mapped_field if mapped_field else [generic_field_name] if generic_field_name else [field.source_name]

    def apply_token(self,
                    token: Union[Field, Keyword, LogicalOperatorType, GroupType],
                    source_mapping: SourceMapping) -> str:
        if isinstance(token, (Field, Keyword)):
            mapped_fields = self.map_field(token, source_mapping) if isinstance(token, Field) else [None]
            if mapped_fields[0] is None:
                token = Keyword(value=token.value)
            elif len(mapped_fields) > 1:
                return self.group_token % self.operator_map[LogicalOperatorType.OR].join([
                    self.field_value_map.apply_field_value(field=field, operator=token.operator, value=token.value)
                    for field in mapped_fields
                ])

            return self.field_value_map.apply_field_value(field=mapped_fields[0],
                                                          operator=token.operator,
                                                          value=token.value)
        elif token.token_type in LogicalOperatorType:
            return self.operator_map.get(token.token_type)
        return token.token_type
