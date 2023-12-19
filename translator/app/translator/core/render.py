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

from abc import ABC
from typing import Union, List, Dict

from app.translator.const import DEFAULT_VALUE_TYPE
from app.translator.core.exceptions.core import NotImplementedException, StrictPlatformException
from app.translator.core.exceptions.parser import UnsupportedOperatorException
from app.translator.core.functions import PlatformFunctions
from app.translator.core.mapping import BasePlatformMappings, SourceMapping, LogSourceSignature, DEFAULT_MAPPING_NAME
from app.translator.core.models.field import Field, Keyword
from app.translator.core.models.functions.base import Function, ParsedFunctions
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.models.parser_output import MetaInfoContainer
from app.translator.core.custom_types.tokens import LogicalOperatorType, OperatorType, GroupType


class BaseQueryFieldValue(ABC):
    details: PlatformDetails = None

    def __init__(self, or_token):
        self.field_value = {
            OperatorType.EQ: self.equal_modifier,
            OperatorType.LT: self.less_modifier,
            OperatorType.LTE: self.less_or_equal_modifier,
            OperatorType.GT: self.greater_modifier,
            OperatorType.GTE: self.greater_or_equal_modifier,
            OperatorType.NEQ: self.not_equal_modifier,
            OperatorType.CONTAINS: self.contains_modifier,
            OperatorType.ENDSWITH: self.endswith_modifier,
            OperatorType.STARTSWITH: self.startswith_modifier,
            OperatorType.REGEX: self.regex_modifier,
            OperatorType.KEYWORD: self.keywords
        }
        self.or_token = f" {or_token} "

    def equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        raise NotImplementedException

    def less_modifier(self, field: str, value: Union[int, str]) -> str:
        raise NotImplementedException

    def less_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:
        raise NotImplementedException

    def greater_modifier(self, field: str, value: Union[int, str]) -> str:
        raise NotImplementedException

    def greater_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:
        raise NotImplementedException

    def not_equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        raise NotImplementedException

    def contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        raise NotImplementedException

    def endswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        raise NotImplementedException

    def startswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        raise NotImplementedException

    def regex_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        raise NotImplementedException

    def keywords(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        raise NotImplementedException

    def apply_field_value(self, field, operator, value):
        if modifier_function := self.field_value.get(operator.token_type):
            return modifier_function(field, value)
        raise UnsupportedOperatorException(operator.token_type)


class BaseQueryRender:
    mappings: BasePlatformMappings = None
    details: PlatformDetails = None
    is_strict_mapping = False
    platform_functions: PlatformFunctions = None

    or_token = "or"
    and_token = "and"
    not_token = "not"

    group_token = "(%s)"

    field_value_map = BaseQueryFieldValue(or_token=or_token)

    query_pattern = '{table} {query} {functions}'

    comment_symbol: str = None
    is_multi_line_comment: bool = False
    unsupported_functions_text = 'Unsupported functions were excluded from the result query:'

    def __init__(self):
        self.operator_map = {
            LogicalOperatorType.AND: f" {self.and_token} ",
            LogicalOperatorType.OR: f" {self.or_token} ",
            LogicalOperatorType.NOT: f" {self.not_token} ",
        }

    def generate_prefix(self, log_source_signature: LogSourceSignature) -> str:
        if str(log_source_signature):
            return f"{str(log_source_signature)} {self.and_token}"
        return ""

    def generate_functions(self, functions: List[Function], source_mapping: SourceMapping) -> str:
        return self.platform_functions.render(functions, source_mapping) if self.platform_functions else ""

    def map_field(self, field: Field, source_mapping: SourceMapping) -> List[str]:
        generic_field_name = field.generic_names_map[source_mapping.source_id]
        # field can be mapped to corresponding platform field name or list of platform field names
        mapped_field = source_mapping.fields_mapping.get_platform_field_name(generic_field_name=generic_field_name)
        if not mapped_field and self.is_strict_mapping:
            raise StrictPlatformException(field_name=field.source_name, platform_name=self.details.name)

        if isinstance(mapped_field, str):
            mapped_field = [mapped_field]

        return mapped_field if mapped_field else [generic_field_name] if generic_field_name else [field.source_name]

    def apply_token(self,
                    token: Union[Field, Keyword, LogicalOperatorType, GroupType],
                    source_mapping: SourceMapping) -> str:
        if isinstance(token, (Field, Keyword)):
            mapped_fields = self.map_field(token, source_mapping) if isinstance(token, Field) else [None]
            if len(mapped_fields) > 1:
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

    def generate_query(self,
                       query: List[Union[Field, Keyword, LogicalOperatorType, GroupType]],
                       source_mapping: SourceMapping) -> str:
        result_values = []
        for token in query:
            result_values.append(self.apply_token(token=token, source_mapping=source_mapping))
        return "".join(result_values)

    def wrap_query_with_meta_info(self, meta_info: MetaInfoContainer, query: str):
        if meta_info and (meta_info.id or meta_info.title):
            query_meta_info = "\n".join(
                self.wrap_with_comment(f"{key}{value}")
                for key, value in {"name: ": meta_info.title, "uuid: ": meta_info.id}.items() if value
            )
            query = f"{query}\n\n{query_meta_info}"
        return query

    def finalize_query(self,
                       prefix: str,
                       query: str,
                       functions: str,
                       meta_info: MetaInfoContainer = None,
                       source_mapping: SourceMapping = None,
                       not_supported_functions: list = None) -> str:
        query = self.query_pattern.format(prefix=prefix, query=query, functions=functions).strip()
        query = self.wrap_query_with_meta_info(meta_info=meta_info, query=query)
        if not_supported_functions:
            rendered_not_supported = self.render_not_supported_functions(not_supported_functions)
            return query + rendered_not_supported
        return query

    def render_not_supported_functions(self, not_supported_functions: list) -> str:
        line_template = f"{self.comment_symbol} " if self.comment_symbol and self.is_multi_line_comment else ""
        not_supported_functions_str = "\n".join(line_template + func.lstrip() for func in not_supported_functions)
        return "\n\n" + self.wrap_with_comment(f"{self.unsupported_functions_text}\n{not_supported_functions_str}")

    def wrap_with_comment(self, value: str) -> str:
        return f"{self.comment_symbol} {value}"

    @staticmethod
    def unique_queries(queries_map: Dict[str, str]) -> Dict[str, List[str]]:
        unique_queries = {}
        for source_id, query in queries_map.items():
            unique_queries.setdefault(query, []).append(source_id)

        return unique_queries

    def finalize(self, queries_map: Dict[str, str]) -> str:
        if len(set(queries_map.values())) == 1:
            return next(iter(queries_map.values()))
        unique_queries = self.unique_queries(queries_map=queries_map)
        result = ""
        for query, source_ids in unique_queries.items():
            result = result + self.wrap_with_comment(", ".join(source_ids)) + f"\n{query}\n\n"

        return result

    def __get_source_mappings(self, source_mapping_ids: List[str]) -> List[SourceMapping]:
        source_mappings = []
        for source_mapping_id in source_mapping_ids:
            if source_mapping := self.mappings.get_source_mapping(source_mapping_id):
                source_mappings.append(source_mapping)

        if not source_mappings:
            source_mappings = [self.mappings.get_source_mapping(DEFAULT_MAPPING_NAME)]

        return source_mappings

    def generate(self, query: list, meta_info: MetaInfoContainer, functions: ParsedFunctions) -> str:
        queries_map = {}
        source_mappings = self.__get_source_mappings(meta_info.source_mapping_ids)

        for source_mapping in source_mappings:
            prefix = self.generate_prefix(source_mapping.log_source_signature)
            result = self.generate_query(query=query, source_mapping=source_mapping)

            finalized_query = self.finalize_query(
                prefix=prefix,
                query=result,
                functions=self.generate_functions(functions.functions, source_mapping),
                not_supported_functions=functions.not_supported,
                meta_info=meta_info,
                source_mapping=source_mapping
            )
            queries_map[source_mapping.source_id] = finalized_query

        return self.finalize(queries_map)
