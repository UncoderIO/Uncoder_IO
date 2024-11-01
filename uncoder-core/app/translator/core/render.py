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
import itertools
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import ClassVar, Optional, Union

from app.translator.const import DEFAULT_VALUE_TYPE
from app.translator.core.const import QUERY_TOKEN_TYPE
from app.translator.core.context_vars import return_only_first_query_ctx_var, wrap_query_with_meta_info_ctx_var
from app.translator.core.custom_types.tokens import LogicalOperatorType, OperatorType
from app.translator.core.custom_types.values import ValueType
from app.translator.core.escape_manager import EscapeManager
from app.translator.core.exceptions.core import StrictPlatformException
from app.translator.core.exceptions.parser import UnsupportedOperatorException
from app.translator.core.exceptions.render import UnsupportedRenderMethod
from app.translator.core.functions import PlatformFunctions
from app.translator.core.mapping import BasePlatformMappings, LogSourceSignature, SourceMapping
from app.translator.core.models.functions.base import Function, RenderedFunctions
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.models.query_container import MetaInfoContainer, RawQueryContainer, TokenizedQueryContainer
from app.translator.core.models.query_tokens.field import Field, PredefinedField
from app.translator.core.models.query_tokens.field_field import FieldField
from app.translator.core.models.query_tokens.field_value import FieldValue
from app.translator.core.models.query_tokens.function_value import FunctionValue
from app.translator.core.models.query_tokens.identifier import Identifier
from app.translator.core.models.query_tokens.keyword import Keyword
from app.translator.core.str_value_manager import StrValue, StrValueManager


class BaseFieldValueRender(ABC):
    details: PlatformDetails = None
    escape_manager: EscapeManager = None
    str_value_manager: StrValueManager = None

    def __init__(self, or_token: str):
        self.modifiers_map: dict[str, Callable[[str, DEFAULT_VALUE_TYPE], str]] = {
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

    @staticmethod
    def _get_value_type(field_name: str, value: Union[int, str, StrValue], value_type: Optional[str] = None) -> str:  # noqa: ARG004
        return value_type or ValueType.value

    @staticmethod
    def _wrap_str_value(value: str) -> str:
        return value

    @staticmethod
    def _wrap_int_value(value: int) -> str:
        return str(value)

    @staticmethod
    def _map_bool_value(value: bool) -> str:
        return "true" if value else "false"

    def _pre_process_value(
        self,
        field: str,
        value: Union[bool, int, str, StrValue],
        value_type: str = ValueType.value,
        wrap_str: bool = False,
        wrap_int: bool = False,
    ) -> Union[int, str]:
        value_type = self._get_value_type(field, value, value_type)
        if isinstance(value, StrValue):
            value = self.str_value_manager.from_container_to_str(value, value_type)
            return self._wrap_str_value(value) if wrap_str else value
        if isinstance(value, str):
            value = self.str_value_manager.escape_manager.escape(value, value_type)
            return self._wrap_str_value(value) if wrap_str else value
        if isinstance(value, bool):
            return self._map_bool_value(value)
        if isinstance(value, int):
            return self._wrap_int_value(value) if wrap_int else value
        return value

    def _pre_process_values_list(
        self, field: str, values: list[Union[int, str, StrValue]], value_type: str = ValueType.value
    ) -> list[str]:
        processed = []
        for val in values:
            value_type = self._get_value_type(field, val, value_type)
            if isinstance(val, StrValue):
                processed.append(self.str_value_manager.from_container_to_str(val, value_type))
            elif isinstance(val, str):
                processed.append(self.str_value_manager.escape_manager.escape(val, value_type))
            else:
                processed.append(str(val))
        return processed

    def equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        raise UnsupportedRenderMethod(platform_name=self.details.name, method=OperatorType.EQ.capitalize())

    def not_equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        raise UnsupportedRenderMethod(platform_name=self.details.name, method=OperatorType.NOT_EQ.capitalize())

    def less_modifier(self, field: str, value: Union[int, str]) -> str:  # noqa: ARG002
        raise UnsupportedRenderMethod(platform_name=self.details.name, method=OperatorType.LT.capitalize())

    def less_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:  # noqa: ARG002
        raise UnsupportedRenderMethod(platform_name=self.details.name, method=OperatorType.LTE.capitalize())

    def greater_modifier(self, field: str, value: Union[int, str]) -> str:  # noqa: ARG002
        raise UnsupportedRenderMethod(platform_name=self.details.name, method=OperatorType.GT.capitalize())

    def greater_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:  # noqa: ARG002
        raise UnsupportedRenderMethod(platform_name=self.details.name, method=OperatorType.GTE.capitalize())

    def contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        raise UnsupportedRenderMethod(platform_name=self.details.name, method=OperatorType.CONTAINS.capitalize())

    def not_contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        raise UnsupportedRenderMethod(platform_name=self.details.name, method=OperatorType.NOT_CONTAINS.capitalize())

    def endswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        raise UnsupportedRenderMethod(platform_name=self.details.name, method=OperatorType.ENDSWITH.capitalize())

    def not_endswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        raise UnsupportedRenderMethod(platform_name=self.details.name, method=OperatorType.NOT_ENDSWITH.capitalize())

    def startswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        raise UnsupportedRenderMethod(platform_name=self.details.name, method=OperatorType.STARTSWITH.capitalize())

    def not_startswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        raise UnsupportedRenderMethod(platform_name=self.details.name, method=OperatorType.NOT_STARTSWITH.capitalize())

    def regex_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        raise UnsupportedRenderMethod(platform_name=self.details.name, method=OperatorType.REGEX.capitalize())

    def not_regex_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        raise UnsupportedRenderMethod(platform_name=self.details.name, method=OperatorType.NOT_REGEX.capitalize())

    def keywords(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        raise UnsupportedRenderMethod(platform_name=self.details.name, method=OperatorType.KEYWORD.capitalize())

    def is_none(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        raise UnsupportedRenderMethod(platform_name=self.details.name, method=OperatorType.IS_NONE.capitalize())

    def is_not_none(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        raise UnsupportedRenderMethod(platform_name=self.details.name, method=OperatorType.IS_NOT_NONE.capitalize())

    def apply_value(self, value: Union[str, int], value_type: str = ValueType.value) -> Union[str, int]:
        return self.escape_manager.escape(value, value_type)

    def apply_field_value(self, field: str, operator: Identifier, value: DEFAULT_VALUE_TYPE) -> str:
        if modifier_function := self.modifiers_map.get(operator.token_type):
            return modifier_function(field, value)
        raise UnsupportedOperatorException(operator.token_type)


class BaseFieldFieldRender(ABC):
    operators_map: ClassVar[dict[str, str]] = {}

    def apply_field_field(self, field_left: str, operator: Identifier, field_right: str) -> str:
        if mapped_operator := self.operators_map.get(operator.token_type):
            return f"{field_left} {mapped_operator} {field_right}"
        raise UnsupportedOperatorException(operator.token_type)


class QueryRender(ABC):
    comment_symbol: str = None
    details: PlatformDetails = None
    is_single_line_comment: bool = False
    unsupported_functions_text = "Unsupported functions were excluded from the result query:"
    unmapped_fields_text = "Unmapped fields: "

    platform_functions: PlatformFunctions = None

    def __init__(self):
        self.init_platform_functions()

    def init_platform_functions(self) -> None:
        self.platform_functions = PlatformFunctions()
        self.platform_functions.platform_query_render = self

    def render_not_supported_functions(self, not_supported_functions: list) -> str:
        line_template = f"{self.comment_symbol} " if self.comment_symbol and self.is_single_line_comment else ""
        not_supported_functions_str = "\n".join(line_template + func.lstrip() for func in not_supported_functions)
        return "\n\n" + self.wrap_with_comment(f"{self.unsupported_functions_text}\n{not_supported_functions_str}")

    def wrap_with_not_supported_functions(self, query: str, not_supported_functions: Optional[list] = None) -> str:
        if not_supported_functions and wrap_query_with_meta_info_ctx_var.get():
            rendered_not_supported = self.render_not_supported_functions(not_supported_functions)
            return query + rendered_not_supported

        return query

    def wrap_with_unmapped_fields(self, query: str, fields: Optional[list[str]]) -> str:
        if wrap_query_with_meta_info_ctx_var.get() and fields:
            return query + "\n\n" + self.wrap_with_comment(f"{self.unmapped_fields_text}{', '.join(fields)}")
        return query

    def wrap_with_comment(self, value: str) -> str:
        return f"{self.comment_symbol} {value}"

    @abstractmethod
    def generate(
        self, raw_query_container: RawQueryContainer, tokenized_query_container: Optional[TokenizedQueryContainer]
    ) -> str:
        raise NotImplementedError("Abstract method")


class PlatformQueryRender(QueryRender):
    mappings: BasePlatformMappings = None

    or_token = "or"
    and_token = "and"
    not_token = "not"

    group_token = "(%s)"
    query_parts_delimiter = " "

    field_field_render = BaseFieldFieldRender()
    field_value_render = BaseFieldValueRender(or_token=or_token)

    predefined_fields_map: ClassVar[dict[str, str]] = {}
    raw_log_field_patterns_map: ClassVar[dict[str, str]] = {}

    def __init__(self):
        super().__init__()
        self.logical_operators_map = {
            LogicalOperatorType.AND: f" {self.and_token} ",
            LogicalOperatorType.OR: f" {self.or_token} ",
            LogicalOperatorType.NOT: f" {self.not_token} ",
        }

    def generate_prefix(self, log_source_signature: Optional[LogSourceSignature], functions_prefix: str = "") -> str:  # noqa: ARG002
        if log_source_signature and str(log_source_signature):
            return f"{log_source_signature} {self.and_token}"
        return ""

    def generate_functions(self, functions: list[Function], source_mapping: SourceMapping) -> RenderedFunctions:
        return self.platform_functions.render(functions, source_mapping)

    def map_predefined_field(self, predefined_field: PredefinedField) -> str:
        if not (mapped_predefined_field_name := self.predefined_fields_map.get(predefined_field.name)):
            if self.mappings.is_strict_mapping:
                raise StrictPlatformException(platform_name=self.details.name, fields=[predefined_field.name])

            return predefined_field.name

        return mapped_predefined_field_name

    def apply_token(self, token: QUERY_TOKEN_TYPE, source_mapping: SourceMapping) -> str:
        if isinstance(token, FieldValue):
            if token.alias:
                mapped_fields = [token.alias.name]
            elif token.predefined_field:
                mapped_fields = [self.map_predefined_field(token.predefined_field)]
            else:
                mapped_fields = self.mappings.map_field(token.field, source_mapping)
            joined = self.logical_operators_map[LogicalOperatorType.OR].join(
                [
                    self.field_value_render.apply_field_value(field=field, operator=token.operator, value=token.value)
                    for field in mapped_fields
                ]
            )
            return self.group_token % joined if len(mapped_fields) > 1 else joined
        if isinstance(token, FieldField):
            alias_left, field_left = token.alias_left, token.field_left
            mapped_fields_left = (
                [alias_left.name] if alias_left else self.mappings.map_field(field_left, source_mapping)
            )
            alias_right, field_right = token.alias_right, token.field_right
            mapped_fields_right = (
                [alias_right.name] if alias_right else self.mappings.map_field(field_right, source_mapping)
            )
            cross_paired_fields = list(itertools.product(mapped_fields_left, mapped_fields_right))
            joined = self.logical_operators_map[LogicalOperatorType.OR].join(
                [
                    self.field_field_render.apply_field_field(pair[0], token.operator, pair[1])
                    for pair in cross_paired_fields
                ]
            )
            return self.group_token % joined if len(cross_paired_fields) > 1 else joined
        if isinstance(token, FunctionValue):
            func_render = self.platform_functions.manager.get_render(token.function.name)
            rendered_func = func_render.render(token.function, source_mapping)
            return self.field_value_render.apply_field_value(
                field=rendered_func, operator=token.operator, value=token.value
            )
        if isinstance(token, Keyword):
            return self.field_value_render.apply_field_value(field="", operator=token.operator, value=token.value)
        if token.token_type in LogicalOperatorType:
            return self.logical_operators_map.get(token.token_type)

        return token.token_type

    def generate_query(self, tokens: list[QUERY_TOKEN_TYPE], source_mapping: SourceMapping) -> str:
        result_values = []
        for token in tokens:
            result_values.append(self.apply_token(token=token, source_mapping=source_mapping))

        return "".join(result_values)

    def wrap_with_meta_info(self, query: str, meta_info: Optional[MetaInfoContainer]) -> str:
        if wrap_query_with_meta_info_ctx_var.get() and meta_info and (meta_info.id or meta_info.title):
            meta_info_dict = {
                "name: ": meta_info.title,
                "uuid: ": meta_info.id,
                "author: ": meta_info.author_str or "not defined in query/rule",
                "licence: ": meta_info.license,
            }
            query_meta_info = "\n".join(
                self.wrap_with_comment(f"{key}{value}") for key, value in meta_info_dict.items() if value
            )
            query = f"{query}\n\n{query_meta_info}"
        return query

    @staticmethod
    def _finalize_search_query(query: str) -> str:
        return query

    def _join_query_parts(self, prefix: str, query: str, functions: str) -> str:
        parts = filter(lambda s: bool(s), map(str.strip, [prefix, self._finalize_search_query(query), functions]))
        return self.query_parts_delimiter.join(parts)

    def finalize_query(
        self,
        prefix: str,
        query: str,
        functions: str,
        meta_info: Optional[MetaInfoContainer] = None,
        source_mapping: Optional[SourceMapping] = None,  # noqa: ARG002
        not_supported_functions: Optional[list] = None,
        unmapped_fields: Optional[list[str]] = None,
        *args,  # noqa: ARG002
        **kwargs,  # noqa: ARG002
    ) -> str:
        query = self._join_query_parts(prefix, query, functions)
        query = self.wrap_with_meta_info(query, meta_info)
        query = self.wrap_with_unmapped_fields(query, unmapped_fields)
        return self.wrap_with_not_supported_functions(query, not_supported_functions)

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

    def generate_from_raw_query_container(self, query_container: RawQueryContainer) -> str:
        return self.finalize_query(
            prefix="", query=query_container.query, functions="", meta_info=query_container.meta_info
        )

    def process_raw_log_field(self, field: str, field_type: str) -> Optional[str]:
        if raw_log_field_pattern := self.raw_log_field_patterns_map.get(field_type):
            return raw_log_field_pattern.format(field=field)

    def process_raw_log_field_prefix(self, field: str, source_mapping: SourceMapping) -> Optional[list]:
        if isinstance(field, list):
            prefix_list = []
            for f in field:
                if _prefix_list := self.process_raw_log_field_prefix(field=f, source_mapping=source_mapping):
                    prefix_list.extend(_prefix_list)
            return prefix_list
        if raw_log_field_type := source_mapping.raw_log_fields.get(field):
            return [self.process_raw_log_field(field=field, field_type=raw_log_field_type)]

    def generate_extra_conditions(self, source_mapping: SourceMapping, tokens: list) -> list:  # noqa: ARG002
        return tokens

    def generate_raw_log_fields(self, fields: list[Field], source_mapping: SourceMapping) -> str:
        if not self.raw_log_field_patterns_map:
            return ""
        defined_raw_log_fields = []
        for field in fields:
            mapped_field = source_mapping.fields_mapping.get_platform_field_name(generic_field_name=field.source_name)
            if not mapped_field:
                generic_field_name = field.get_generic_field_name(source_mapping.source_id)
                mapped_field = source_mapping.fields_mapping.get_platform_field_name(
                    generic_field_name=generic_field_name
                )
            if not mapped_field and self.mappings.is_strict_mapping:
                raise StrictPlatformException(
                    platform_name=self.details.name, fields=[field.source_name], mapping=source_mapping.source_id
                )
            if prefix_list := self.process_raw_log_field_prefix(field=mapped_field, source_mapping=source_mapping):
                for prefix in prefix_list:
                    if prefix not in defined_raw_log_fields:
                        defined_raw_log_fields.append(prefix)
        return "\n".join(defined_raw_log_fields)

    def _generate_from_tokenized_query_container_by_source_mapping(
        self, query_container: TokenizedQueryContainer, source_mapping: SourceMapping
    ) -> str:
        unmapped_fields = self.mappings.check_fields_mapping_existence(
            query_container.meta_info.query_fields,
            query_container.meta_info.function_fields_map,
            self.platform_functions.manager.supported_render_names,
            source_mapping,
        )
        rendered_functions = self.generate_functions(query_container.functions.functions, source_mapping)
        prefix = self.generate_prefix(source_mapping.log_source_signature, rendered_functions.rendered_prefix)

        if source_mapping.raw_log_fields:
            defined_raw_log_fields = self.generate_raw_log_fields(
                fields=query_container.meta_info.query_fields + query_container.meta_info.function_fields,
                source_mapping=source_mapping,
            )
            prefix += f"\n{defined_raw_log_fields}"
        if source_mapping.conditions:
            query_container.tokens = self.generate_extra_conditions(
                source_mapping=source_mapping, tokens=query_container.tokens
            )
        query = self.generate_query(tokens=query_container.tokens, source_mapping=source_mapping)
        not_supported_functions = query_container.functions.not_supported + rendered_functions.not_supported
        return self.finalize_query(
            prefix=prefix,
            query=query,
            functions=rendered_functions.rendered,
            not_supported_functions=not_supported_functions,
            unmapped_fields=unmapped_fields,
            meta_info=query_container.meta_info,
            source_mapping=source_mapping,
        )

    def generate_from_tokenized_query_container(self, query_container: TokenizedQueryContainer) -> str:
        queries_map = {}
        errors = []
        source_mappings = self.mappings.get_source_mappings_by_ids(query_container.meta_info.source_mapping_ids)

        for source_mapping in source_mappings:
            try:
                finalized_query = self._generate_from_tokenized_query_container_by_source_mapping(
                    query_container, source_mapping
                )
                if return_only_first_query_ctx_var.get() is True:
                    return finalized_query
                queries_map[source_mapping.source_id] = finalized_query
            except StrictPlatformException as err:
                errors.append(err)
                continue

        if not queries_map and errors:
            raise errors[0]
        return self.finalize(queries_map)

    def generate(
        self, raw_query_container: RawQueryContainer, tokenized_query_container: Optional[TokenizedQueryContainer]
    ) -> str:
        if tokenized_query_container:
            return self.generate_from_tokenized_query_container(tokenized_query_container)
        return self.generate_from_raw_query_container(raw_query_container)
