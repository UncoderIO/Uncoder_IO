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
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Optional, Union

from app.translator.const import DEFAULT_VALUE_TYPE
from app.translator.core.custom_types.tokens import LogicalOperatorType, OperatorType
from app.translator.core.custom_types.values import ValueType
from app.translator.core.escape_manager import EscapeManager
from app.translator.core.exceptions.core import NotImplementedException, StrictPlatformException
from app.translator.core.exceptions.parser import UnsupportedOperatorException
from app.translator.core.functions import PlatformFunctions
from app.translator.core.mapping import DEFAULT_MAPPING_NAME, BasePlatformMappings, LogSourceSignature, SourceMapping
from app.translator.core.models.field import Field, FieldValue, Keyword
from app.translator.core.models.functions.base import Function, RenderedFunctions
from app.translator.core.models.identifier import Identifier
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.models.query_container import MetaInfoContainer, RawQueryContainer, TokenizedQueryContainer
from app.translator.core.str_value_manager import StrValueManager
from app.translator.core.tokenizer import TOKEN_TYPE


class BaseQueryFieldValue(ABC):
    details: PlatformDetails = None
    escape_manager: EscapeManager = None
    str_value_manager: StrValueManager = None

    def __init__(self, or_token: str):
        self.field_value: dict[str, Callable[[str, DEFAULT_VALUE_TYPE], str]] = {
            OperatorType.EQ: self.equal_modifier,
            OperatorType.NOT_EQ: self.not_equal_modifier,
            OperatorType.LT: self.less_modifier,
            OperatorType.LTE: self.less_or_equal_modifier,
            OperatorType.GT: self.greater_modifier,
            OperatorType.GTE: self.greater_or_equal_modifier,
            OperatorType.CONTAINS: self.contains_modifier,
            OperatorType.NOT_CONTAINS: self.not_contains_modifier,
            OperatorType.ENDSWITH: self.endswith_modifier,
            OperatorType.NOT_ENDSWITH: self.not_endswith_modifier,
            OperatorType.STARTSWITH: self.startswith_modifier,
            OperatorType.NOT_STARTSWITH: self.not_startswith_modifier,
            OperatorType.REGEX: self.regex_modifier,
            OperatorType.NOT_REGEX: self.not_regex_modifier,
            OperatorType.KEYWORD: self.keywords,
            OperatorType.IS_NONE: self.is_none,
            OperatorType.IS_NOT_NONE: self.is_not_none,
        }
        self.or_token = f" {or_token} "

    def equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        raise NotImplementedException

    def not_equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        raise NotImplementedException

    def less_modifier(self, field: str, value: Union[int, str]) -> str:  # noqa: ARG002
        raise NotImplementedException

    def less_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:  # noqa: ARG002
        raise NotImplementedException

    def greater_modifier(self, field: str, value: Union[int, str]) -> str:  # noqa: ARG002
        raise NotImplementedException

    def greater_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:  # noqa: ARG002
        raise NotImplementedException

    def contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        raise NotImplementedException

    def not_contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        raise NotImplementedException

    def endswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        raise NotImplementedException

    def not_endswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        raise NotImplementedException

    def startswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        raise NotImplementedException

    def not_startswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        raise NotImplementedException

    def regex_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        raise NotImplementedException

    def not_regex_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        raise NotImplementedException

    def keywords(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        raise NotImplementedException

    def is_none(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        raise NotImplementedException

    def is_not_none(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        raise NotImplementedException

    def apply_value(self, value: Union[str, int], value_type: str = ValueType.value) -> Union[str, int]:
        return self.escape_manager.escape(value, value_type)

    def apply_field_value(self, field: str, operator: Identifier, value: DEFAULT_VALUE_TYPE) -> str:
        if modifier_function := self.field_value.get(operator.token_type):
            return modifier_function(field, value)
        raise UnsupportedOperatorException(operator.token_type)


class QueryRender(ABC):
    @abstractmethod
    def generate(self, query_container: Union[RawQueryContainer, TokenizedQueryContainer]) -> str:
        raise NotImplementedError("Abstract method")


class PlatformQueryRender(QueryRender):
    mappings: BasePlatformMappings = None
    details: PlatformDetails = None
    is_strict_mapping = False
    platform_functions: PlatformFunctions = PlatformFunctions()

    or_token = "or"
    and_token = "and"
    not_token = "not"

    group_token = "(%s)"

    field_value_map = BaseQueryFieldValue(or_token=or_token)

    query_pattern = "{table} {query} {functions}"

    comment_symbol: str = None
    is_multi_line_comment: bool = False
    unsupported_functions_text = "Unsupported functions were excluded from the result query:"

    def __init__(self):
        self.operator_map = {
            LogicalOperatorType.AND: f" {self.and_token} ",
            LogicalOperatorType.OR: f" {self.or_token} ",
            LogicalOperatorType.NOT: f" {self.not_token} ",
        }

    def generate_prefix(self, log_source_signature: LogSourceSignature) -> str:
        if str(log_source_signature):
            return f"{log_source_signature!s} {self.and_token}"
        return ""

    def generate_functions(self, functions: list[Function], source_mapping: SourceMapping) -> RenderedFunctions:
        return self.platform_functions.render(functions, source_mapping)

    def map_field(self, field: Field, source_mapping: SourceMapping) -> list[str]:
        generic_field_name = field.get_generic_field_name(source_mapping.source_id)
        # field can be mapped to corresponding platform field name or list of platform field names
        mapped_field = source_mapping.fields_mapping.get_platform_field_name(generic_field_name=generic_field_name)
        if not mapped_field and self.is_strict_mapping:
            raise StrictPlatformException(field_name=field.source_name, platform_name=self.details.name)

        if isinstance(mapped_field, str):
            mapped_field = [mapped_field]

        return mapped_field if mapped_field else [generic_field_name] if generic_field_name else [field.source_name]

    def apply_token(self, token: Union[FieldValue, Keyword, Identifier], source_mapping: SourceMapping) -> str:
        if isinstance(token, FieldValue):
            mapped_fields = self.map_field(token.field, source_mapping)
            if len(mapped_fields) > 1:
                return self.group_token % self.operator_map[LogicalOperatorType.OR].join(
                    [
                        self.field_value_map.apply_field_value(field=field, operator=token.operator, value=token.value)
                        for field in mapped_fields
                    ]
                )

            return self.field_value_map.apply_field_value(
                field=mapped_fields[0], operator=token.operator, value=token.value
            )

        if isinstance(token, Keyword):
            return self.field_value_map.apply_field_value(field=None, operator=token.operator, value=token.value)
        if token.token_type in LogicalOperatorType:
            return self.operator_map.get(token.token_type)

        return token.token_type

    def generate_query(self, tokens: list[TOKEN_TYPE], source_mapping: SourceMapping) -> str:
        result_values = []
        for token in tokens:
            result_values.append(self.apply_token(token=token, source_mapping=source_mapping))
        return "".join(result_values)

    def wrap_query_with_meta_info(self, meta_info: MetaInfoContainer, query: str) -> str:
        if meta_info and (meta_info.id or meta_info.title):
            meta_info_dict = {
                "name: ": meta_info.title,
                "uuid: ": meta_info.id,
                "author: ": meta_info.author if meta_info.author else "not defined in query/rule",
                "licence: ": meta_info.license,
            }
            query_meta_info = "\n".join(
                self.wrap_with_comment(f"{key}{value}") for key, value in meta_info_dict.items() if value
            )
            query = f"{query}\n\n{query_meta_info}"
        return query

    def finalize_query(
        self,
        prefix: str,
        query: str,
        functions: str,
        meta_info: Optional[MetaInfoContainer] = None,
        source_mapping: Optional[SourceMapping] = None,  # noqa: ARG002
        not_supported_functions: Optional[list] = None,
        *args,  # noqa: ARG002
        **kwargs,  # noqa: ARG002
    ) -> str:
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
    def unique_queries(queries_map: dict[str, str]) -> dict[str, dict[str]]:
        unique_queries = {}
        for source_id, query in queries_map.items():
            unique_queries.setdefault(query, []).append(source_id)

        return unique_queries

    def finalize(self, queries_map: dict[str, str]) -> str:
        if len(set(queries_map.values())) == 1:
            return next(iter(queries_map.values()))
        unique_queries = self.unique_queries(queries_map=queries_map)
        result = ""
        for query, source_ids in unique_queries.items():
            result = result + self.wrap_with_comment(", ".join(source_ids)) + f"\n{query}\n\n"

        return result

    def _get_source_mappings(self, source_mapping_ids: list[str]) -> list[SourceMapping]:
        source_mappings = []
        for source_mapping_id in source_mapping_ids:
            if source_mapping := self.mappings.get_source_mapping(source_mapping_id):
                source_mappings.append(source_mapping)

        if not source_mappings:
            source_mappings = [self.mappings.get_source_mapping(DEFAULT_MAPPING_NAME)]

        return source_mappings

    def _generate_from_raw_query_container(self, query_container: RawQueryContainer) -> str:
        return self.finalize_query(
            prefix="", query=query_container.query, functions="", meta_info=query_container.meta_info
        )

    def _generate_from_tokenized_query_container(self, query_container: TokenizedQueryContainer) -> str:
        queries_map = {}
        source_mappings = self._get_source_mappings(query_container.meta_info.source_mapping_ids)

        for source_mapping in source_mappings:
            prefix = self.generate_prefix(source_mapping.log_source_signature)
            result = self.generate_query(tokens=query_container.tokens, source_mapping=source_mapping)
            rendered_functions = self.generate_functions(query_container.functions.functions, source_mapping)
            not_supported_functions = query_container.functions.not_supported + rendered_functions.not_supported
            finalized_query = self.finalize_query(
                prefix=prefix,
                query=result,
                functions=rendered_functions.rendered,
                not_supported_functions=not_supported_functions,
                meta_info=query_container.meta_info,
                source_mapping=source_mapping,
            )
            queries_map[source_mapping.source_id] = finalized_query

        return self.finalize(queries_map)

    def generate(self, query_container: Union[RawQueryContainer, TokenizedQueryContainer]) -> str:
        if isinstance(query_container, RawQueryContainer):
            return self._generate_from_raw_query_container(query_container)

        return self._generate_from_tokenized_query_container(query_container)
