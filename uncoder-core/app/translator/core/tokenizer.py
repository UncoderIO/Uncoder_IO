"""
Uncoder IO Commercial Edition License
-----------------------------------------------------------------
Copyright (c) 2024 SOC Prime, Inc.

This file is part of the Uncoder IO Commercial Edition ("CE") and is
licensed under the Uncoder IO Non-Commercial License (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://github.com/UncoderIO/UncoderIO/blob/main/LICENSE

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-----------------------------------------------------------------
"""

import re
from abc import ABC, abstractmethod
from typing import Any, ClassVar, Optional, Union

from app.translator.core.const import QUERY_TOKEN_TYPE
from app.translator.core.custom_types.tokens import GroupType, LogicalOperatorType, OperatorType
from app.translator.core.custom_types.values import ValueType
from app.translator.core.escape_manager import EscapeManager
from app.translator.core.exceptions.functions import NotSupportedFunctionException
from app.translator.core.exceptions.parser import (
    QueryParenthesesException,
    TokenizerGeneralException,
    UnsupportedOperatorException,
)
from app.translator.core.functions import PlatformFunctions
from app.translator.core.mapping import SourceMapping
from app.translator.core.models.field import Field, FieldField, FieldValue, Keyword
from app.translator.core.models.function_value import FunctionValue
from app.translator.core.models.functions.base import Function
from app.translator.core.models.functions.eval import EvalArg
from app.translator.core.models.functions.group_by import GroupByFunction
from app.translator.core.models.functions.join import JoinFunction
from app.translator.core.models.functions.rename import RenameArg
from app.translator.core.models.functions.sort import SortArg
from app.translator.core.models.functions.union import UnionFunction
from app.translator.core.models.identifier import Identifier
from app.translator.core.str_value_manager import StrValue, StrValueManager
from app.translator.tools.utils import get_match_group


class BaseTokenizer(ABC):
    @abstractmethod
    def tokenize(self, query: str) -> list[Union[FieldValue, Keyword, Identifier]]:
        raise NotImplementedError


class QueryTokenizer(BaseTokenizer):
    # used to generate re pattern. so the keys order is important
    single_value_operators_map: ClassVar[dict[str, str]] = {}
    # used to generate re pattern. so the keys order is important
    multi_value_operators_map: ClassVar[dict[str, str]] = {}
    # used to generate re pattern. so the keys order is important
    fields_operator_map: ClassVar[dict[str, str]] = {}
    operators_map: ClassVar[dict[str, str]] = {}  # used to generate re pattern. so the keys order is important

    logical_operator_pattern = r"^(?P<logical_operator>and|or|not|AND|OR|NOT)\s+"
    field_value_pattern = r"""^___field___\s*___operator___\s*___value___"""
    base_value_pattern = r"(?:___value_pattern___)"

    # do not modify, use subclasses to define this attribute
    field_pattern: str = None
    function_pattern: str = None
    _value_pattern: str = None
    value_pattern: str = None
    multi_value_pattern: str = None
    keyword_pattern: str = None
    multi_value_delimiter_pattern = r","

    wildcard_symbol = None
    escape_manager: EscapeManager = None
    str_value_manager: StrValueManager = None
    platform_functions: PlatformFunctions = None

    def __init_subclass__(cls, **kwargs):
        cls._validate_re_patterns()
        cls.value_pattern = cls.base_value_pattern.replace("___value_pattern___", cls._value_pattern)
        cls.operators_map = {
            **cls.single_value_operators_map,
            **cls.multi_value_operators_map,
            **cls.fields_operator_map,
        }
        cls.operator_pattern = rf"""(?:___field___\s*(?P<operator>(?:{'|'.join(cls.operators_map)})))\s*"""

    @classmethod
    def _validate_re_patterns(cls) -> None:
        if not all([cls.field_pattern, cls._value_pattern]):
            raise ValueError(f"{cls.__name__} re patterns must be set")

    def map_operator(self, operator: str) -> str:
        try:
            return self.operators_map[operator.lower()]
        except KeyError as e:
            raise UnsupportedOperatorException(operator) from e

    def search_field(self, query: str) -> str:
        field_search = re.search(self.field_pattern, query)
        if field_search is None:
            raise TokenizerGeneralException(error=f"Field couldn't be found in query part: {query}")
        return field_search.group("field_name")

    def escape_field_name(self, field_name: str) -> str:
        return field_name.replace(".", r"\.")

    def search_operator(self, query: str, field_name: str) -> str:
        field_name = self.escape_field_name(field_name)
        operator_pattern = self.operator_pattern.replace("___field___", field_name)
        compiled_operator_regex = re.compile(operator_pattern, re.IGNORECASE)
        if (operator_search := re.search(compiled_operator_regex, query)) is None:
            raise TokenizerGeneralException(error=f"Operator couldn't be found in query part: {query}")

        operator = operator_search.group("operator")
        return operator.strip(" ")

    def get_operator_and_value(
        self,
        match: re.Match,
        mapped_operator: str = OperatorType.EQ,
        operator: Optional[str] = None,  # noqa: ARG002
    ) -> tuple[str, Any]:
        return mapped_operator, get_match_group(match, group_name=ValueType.value)

    @staticmethod
    def clean_multi_value(value: str) -> str:
        value = value.strip(" ")
        if value.startswith("'") and value.endswith("'") or value.startswith('"') and value.endswith('"'):
            value = value[1:-1]

        return value

    def search_single_value(self, query: str, operator: str, field_name: str) -> tuple[str, str, Union[str, StrValue]]:
        field_value_match = self._get_field_value_match(query, operator, field_name, self.value_pattern)
        mapped_operator, value = self.get_operator_and_value(field_value_match, self.map_operator(operator), operator)
        if self.should_process_value_wildcards(operator):
            mapped_operator, value = self.process_value_wildcards(value, mapped_operator)

        pos = field_value_match.end()
        return query[pos:], mapped_operator, value

    def search_multi_value(
        self, query: str, operator: str, field_name: str
    ) -> tuple[str, dict[str, list[Union[str, StrValue]]]]:
        field_value_match = self._get_field_value_match(query, operator, field_name, self.multi_value_pattern)
        if (multi_value := get_match_group(field_value_match, group_name=ValueType.multi_value)) is None:
            raise TokenizerGeneralException(error=f"Value couldn't be found in query part: {query}")

        values = [self.clean_multi_value(v) for v in re.split(self.multi_value_delimiter_pattern, multi_value)]
        grouped_values = self.group_values_by_operator(values, operator)
        pos = field_value_match.end()
        return query[pos:], grouped_values

    def _get_field_value_match(self, query: str, operator: str, field_name: str, value_pattern: str) -> re.Match:
        field_value_pattern = self.get_field_value_pattern(operator, field_name, value_pattern)
        field_value_regex = re.compile(field_value_pattern, re.IGNORECASE)
        field_value_match = re.match(field_value_regex, query)
        if field_value_match is None:
            raise TokenizerGeneralException(error=f"Value couldn't be found in query part: {query}")

        return field_value_match

    def group_values_by_operator(self, values: list[str], operator: str) -> dict[str, list[str]]:
        mapped_operator = self.map_operator(operator)
        result = {}
        for value in values:
            op = mapped_operator
            if self.should_process_value_wildcards(operator):
                op, value = self.process_value_wildcards(value, mapped_operator)
            result.setdefault(op, []).append(value)

        return result

    def search_keyword(self, query: str) -> tuple[Keyword, str]:
        keyword_search = re.search(self.keyword_pattern, query)
        _, value = self.get_operator_and_value(keyword_search)
        keyword = Keyword(value=value)
        pos = keyword_search.end()
        return keyword, query[pos:]

    def get_field_value_pattern(self, operator: str, field_name: str, value_pattern: str) -> str:
        field_value_pattern = self.field_value_pattern.replace("___field___", self.escape_field_name(field_name))
        field_value_pattern = field_value_pattern.replace("___operator___", operator)
        return field_value_pattern.replace("___value___", value_pattern)

    @staticmethod
    def should_process_value_wildcards(operator: Optional[str]) -> bool:  # noqa: ARG004
        return True

    def process_value_wildcards(
        self, value: Union[str, StrValue], operator: str = OperatorType.EQ
    ) -> tuple[str, Union[str, StrValue]]:
        if not (wildcard := self.wildcard_symbol) or operator == OperatorType.REGEX or len(value) == 1:
            return operator, value

        if value.startswith(wildcard) and value.endswith(wildcard):
            if isinstance(value, StrValue):
                value = StrValue(value.strip(wildcard), value.split_value[1:-1])
            else:
                value = value.strip(wildcard)
            return OperatorType.CONTAINS, value

        if value.startswith(wildcard):
            if isinstance(value, StrValue):
                value = StrValue(value.lstrip(wildcard), value.split_value[1:])
            else:
                value = value.lstrip(wildcard)
            return OperatorType.ENDSWITH, value

        if value.endswith(wildcard):
            if isinstance(value, StrValue):
                value = StrValue(value.rstrip(wildcard), value.split_value[:-1])
            else:
                value = value.rstrip(wildcard)
            return OperatorType.STARTSWITH, value

        return operator, value

    @staticmethod
    def create_field_value(field_name: str, operator: Identifier, value: Union[str, list]) -> FieldValue:
        return FieldValue(source_name=field_name, operator=operator, value=value)

    @staticmethod
    def concat_field_value_tokens(tokens: list[FieldValue]) -> list[Union[FieldValue, Identifier]]:
        result = [tokens[0]]
        for token in tokens[1:]:
            result.append(Identifier(token_type=LogicalOperatorType.OR))
            result.append(token)

        return result

    def is_multi_value_flow(self, field_name: str, operator: str, query: str) -> bool:  # noqa: ARG002
        return operator.lower() in self.multi_value_operators_map

    def search_field_value(self, query: str) -> tuple[Union[FieldValue, list[Union[FieldValue, Identifier]]], str]:
        field_name = self.search_field(query)
        operator = self.search_operator(query, field_name)
        if self.is_multi_value_flow(field_name, operator, query):
            query, grouped_values = self.search_multi_value(query=query, operator=operator, field_name=field_name)
            tokens = [
                self.create_field_value(field_name=field_name, operator=Identifier(token_type=op), value=values)
                for op, values in grouped_values.items()
            ]
            if len(tokens) > 1:
                l_paren = Identifier(token_type=GroupType.L_PAREN)
                r_paren = Identifier(token_type=GroupType.R_PAREN)
                tokens = [l_paren, *self.concat_field_value_tokens(tokens), r_paren]

            return tokens, query

        query, operator, value = self.search_single_value(query=query, operator=operator, field_name=field_name)
        operator_token = Identifier(token_type=operator)
        field_value = self.create_field_value(field_name=field_name, operator=operator_token, value=value)
        return field_value, query

    def _check_field_value_match(self, query: str, white_space_pattern: str = r"\s+") -> bool:
        single_value_operator_group = rf"(?:{'|'.join(self.single_value_operators_map)})"
        single_value_pattern = rf"""{self.field_pattern}\s*{single_value_operator_group}\s*{self.value_pattern}\s*"""
        if re.match(single_value_pattern, query, re.IGNORECASE):
            return True

        if self.multi_value_operators_map:
            multi_value_operator_group = rf"(?:{'|'.join(self.multi_value_operators_map)})"
            pattern = f"{self.field_pattern}{white_space_pattern}{multi_value_operator_group}{white_space_pattern}"
            multi_value_pattern = rf"{pattern}{self.multi_value_pattern}"
            if re.match(multi_value_pattern, query, re.IGNORECASE):
                return True

        return False

    def search_function_value(self, query: str) -> tuple[FunctionValue, str]:  # noqa: ARG002
        raise NotSupportedFunctionException

    @staticmethod
    def _check_function_value_match(query: str) -> bool:  # noqa: ARG004
        return False

    def _get_next_token(
        self, query: str
    ) -> tuple[Union[FieldValue, FunctionValue, Keyword, Identifier, list[Union[FieldValue, Identifier]]], str]:
        query = query.strip("\n").strip(" ").strip("\n")
        if query.startswith(GroupType.L_PAREN):
            return Identifier(token_type=GroupType.L_PAREN), query[1:]
        if query.startswith(GroupType.R_PAREN):
            return Identifier(token_type=GroupType.R_PAREN), query[1:]
        if logical_operator_search := re.match(self.logical_operator_pattern, query):
            logical_operator = logical_operator_search.group("logical_operator")
            pos = logical_operator_search.end()
            return Identifier(token_type=logical_operator.lower()), query[pos:]
        if self.platform_functions and self._check_function_value_match(query):
            return self.search_function_value(query)
        if self._check_field_value_match(query):
            return self.search_field_value(query)
        if self.keyword_pattern and re.match(self.keyword_pattern, query):
            return self.search_keyword(query)

        raise TokenizerGeneralException("Unsupported query entry")

    @staticmethod
    def _validate_parentheses(tokens: list[QUERY_TOKEN_TYPE]) -> None:
        parentheses = []
        for token in tokens:
            if isinstance(token, Identifier) and token.token_type in (GroupType.L_PAREN, GroupType.R_PAREN):
                if token.token_type == GroupType.L_PAREN:
                    parentheses.append(token)
                elif not parentheses or parentheses[-1].token_type == GroupType.R_PAREN:
                    raise QueryParenthesesException
                else:
                    parentheses.pop()
        if parentheses:
            raise QueryParenthesesException

    def tokenize(self, query: str) -> list[Union[FieldValue, Keyword, Identifier]]:
        tokenized = []
        while query:
            next_token, sliced_query = self._get_next_token(query=query)
            if isinstance(next_token, list):
                tokenized.extend(next_token)
            else:
                tokenized.append(next_token)

            if len(sliced_query) >= len(query):
                raise TokenizerGeneralException("Unsupported query entry. Infinite loop")

            query = sliced_query

        self._validate_parentheses(tokenized)
        return tokenized

    @staticmethod
    def filter_tokens(
        tokens: list[QUERY_TOKEN_TYPE],
        token_type: Union[type[FieldValue], type[Field], type[Keyword], type[Identifier]],
    ) -> list[QUERY_TOKEN_TYPE]:
        return [token for token in tokens if isinstance(token, token_type)]

    def get_field_tokens_from_func_args(  # noqa: PLR0912
        self, args: list[Union[Field, FieldValue, Keyword, Identifier, Function, SortArg]]
    ) -> list[Field]:
        result = []
        for arg in args:
            if isinstance(arg, Field):
                result.append(arg)
            elif isinstance(arg, FieldField):
                if arg.field_left:
                    result.append(arg.field_left)
                if arg.field_right:
                    result.append(arg.field_right)
            elif isinstance(arg, FieldValue):
                if arg.field:
                    result.append(arg.field)
            elif isinstance(arg, FunctionValue):
                result.extend(self.get_field_tokens_from_func_args(args=[arg.function]))
            elif isinstance(arg, GroupByFunction):
                result.extend(self.get_field_tokens_from_func_args(args=arg.args))
                result.extend(self.get_field_tokens_from_func_args(args=arg.by_clauses))
                result.extend(self.get_field_tokens_from_func_args(args=[arg.filter_]))
            elif isinstance(arg, (JoinFunction, UnionFunction)):
                continue
            elif isinstance(arg, Function):
                result.extend(self.get_field_tokens_from_func_args(args=arg.args))
            elif isinstance(arg, SortArg) and isinstance(arg.field, Field):
                result.append(arg.field)
            elif isinstance(arg, RenameArg):
                result.append(arg.field_)
            elif isinstance(arg, EvalArg):
                if isinstance(arg.field_, Field):
                    result.append(arg.field_)
                result.extend(self.get_field_tokens_from_func_args(args=arg.expression))
        return result

    @staticmethod
    def set_field_tokens_generic_names_map(
        tokens: list[Field], source_mappings: list[SourceMapping], default_mapping: SourceMapping
    ) -> None:
        for token in tokens:
            token.set_generic_names_map(source_mappings, default_mapping)
