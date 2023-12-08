"""
Uncoder IO Commercial Edition License
-----------------------------------------------------------------
Copyright (c) 2023 SOC Prime, Inc.

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

from abc import ABC, abstractmethod
import re
from typing import Tuple, Union, List, Any, Optional, Type

from app.translator.core.exceptions.parser import (
    UnsupportedOperatorException,
    TokenizerGeneralException,
    QueryParenthesesException
)
from app.translator.core.mapping import SourceMapping, DEFAULT_MAPPING_NAME, BasePlatformMappings
from app.translator.core.models.field import Field, Keyword
from app.translator.core.models.functions.base import Function
from app.translator.core.models.functions.sort import SortArg
from app.translator.core.models.identifier import Identifier
from app.translator.core.custom_types.tokens import OperatorType, GroupType
from app.translator.tools.utils import get_match_group

TOKEN_TYPE = Union[Field, Keyword, Identifier]


class BaseTokenizer(ABC):
    @abstractmethod
    def tokenize(self, query: str) -> List[Union[Field, Keyword, Identifier]]:
        raise NotImplementedError()


class QueryTokenizer(BaseTokenizer):
    field_pattern = r"(?P<field_name>[a-zA-Z\._\-]+)"
    operator_pattern = r"\s?(?P<operator>and|or|not|AND|OR|NOT)\s?"
    field_value_pattern = r"""^___field___\s*___match_operator___\s*___value___"""
    match_operator_pattern = r"""(?:___field___\s?(?P<match_operator>ilike|contains|endswith|startswith|in|>=|<=|==|>|<|=~|!=|=|:|\:))\s?"""
    base_value_pattern = r"(?:___value_pattern___)"
    _value_pattern = r"""(?:\"|\')*(?P<value>[:a-zA-Z\*0-9=+%#\-_\/\\'\,.&^@!\(\s]*)(?:\*|\'|\"|\s|\$)*"""
    value_pattern = base_value_pattern.replace('___value_pattern___', _value_pattern)
    multi_value_pattern = r"""\((?P<value>[:a-zA-Z\"\*0-9=+%#\-_\/\\'\,.&^@!\(\s]*)\)"""
    keyword_pattern = None  # do not modify, use subclasses to define this attribute

    multi_value_operators = tuple()
    multi_value_delimiter = ","
    wildcard_symbol = None

    operators_map = {
        "=": OperatorType.EQ,
        "in": OperatorType.EQ,
        "<": OperatorType.LT,
        "<=": OperatorType.LTE,
        ">": OperatorType.GT,
        ">=": OperatorType.GTE,
        "!=": OperatorType.NEQ,
        "contains": OperatorType.CONTAINS,
        "startswith": OperatorType.STARTSWITH,
        "endswith": OperatorType.ENDSWITH
    }

    def __init_subclass__(cls, **kwargs):
        cls.value_pattern = cls.base_value_pattern.replace('___value_pattern___', cls._value_pattern)

    def map_operator(self, operator: str) -> str:
        try:
            return self.operators_map[operator.lower()]
        except KeyError as e:
            raise UnsupportedOperatorException(operator)

    def search_field(self, query):
        field_search = re.search(self.field_pattern, query)
        if field_search is None:
            raise TokenizerGeneralException(error=f"Field couldn't be found in query part: {query}")
        field = field_search.group("field_name")
        return field

    def escape_field_name(self, field_name):
        return field_name.replace(".", r"\.")

    def search_match_operator(self, query, field_name) -> str:
        field_name = self.escape_field_name(field_name)
        match_operator_pattern = self.match_operator_pattern.replace("___field___", field_name)
        match_operator_regex = re.compile(match_operator_pattern, re.IGNORECASE)
        match_operator_search = re.search(match_operator_regex, query)
        if match_operator_search is None:
            raise TokenizerGeneralException(error=f"Operator couldn't be found in query part: {query}")
        match_operator = match_operator_search.group("match_operator")
        match_operator = match_operator.strip(" ")
        return match_operator

    def get_operator_and_value(self, match: re.Match, operator: str = OperatorType.EQ) -> Tuple[str, Any]:
        return operator, get_match_group(match, group_name='value')

    @staticmethod
    def clean_multi_value(value: Union[int, str]) -> Union[int, str]:
        if isinstance(value, str):
            value = value.strip(" ")
            if value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            elif value.startswith('"') and value.endswith('"'):
                value = value[1:-1]

        return value

    def search_value(self, query: str, operator: str, field_name: str) -> Tuple[str, str, Any]:
        field_value_pattern = self.get_field_value_pattern(operator, field_name)
        value_pattern = self.value_pattern
        is_multi = False
        if operator.lower() in self.multi_value_operators:
            value_pattern = self.multi_value_pattern
            is_multi = True

        field_value_pattern = field_value_pattern.replace("___value___", value_pattern)
        field_value_regex = re.compile(field_value_pattern, re.IGNORECASE)
        field_value_search = re.match(field_value_regex, query)
        if field_value_search is None:
            raise TokenizerGeneralException(error=f"Value couldn't be found in query part: {query}")

        operator, value = self.get_operator_and_value(field_value_search, self.map_operator(operator))
        value = [self.clean_multi_value(v) for v in value.split(",")] if is_multi else value
        pos = field_value_search.end()
        return query[pos:], operator, value

    def search_keyword(self, query: str) -> Tuple[Keyword, str]:
        keyword_search = re.search(self.keyword_pattern, query)
        _, value = self.get_operator_and_value(keyword_search)
        keyword = Keyword(value=value)
        pos = keyword_search.end()
        return keyword, query[pos:]

    def get_field_value_pattern(self, operator, field_name):
        field_value_pattern = self.field_value_pattern.replace("___field___", self.escape_field_name(field_name))
        return field_value_pattern.replace("___match_operator___", operator)

    @staticmethod
    def _clean_value(value: str, wildcard_symbol: str) -> str:
        return value.strip(wildcard_symbol) if wildcard_symbol else value

    @staticmethod
    def __get_operator_token(value: str, operator: str, wildcard_symbol: str) -> Identifier:
        if not wildcard_symbol:
            return Identifier(token_type=operator)

        if operator == OperatorType.REGEX:
            if not (value.startswith(wildcard_symbol) and value.endswith(wildcard_symbol)):
                return Identifier(token_type=OperatorType.REGEX)

        if value.startswith(wildcard_symbol) and value.endswith(wildcard_symbol):
            return Identifier(token_type=OperatorType.CONTAINS)
        elif value.startswith(wildcard_symbol):
            return Identifier(token_type=OperatorType.ENDSWITH)
        elif value.endswith(wildcard_symbol):
            return Identifier(token_type=OperatorType.STARTSWITH)
        else:
            return Identifier(token_type=operator)

    def process_value_wildcard_symbols(self,
                                       value: Union[List[str], str],
                                       operator: str,
                                       wildcard_symbol: Optional[str]) -> Tuple[Union[List[str], str], Identifier]:
        if isinstance(value, list):
            op = self.__get_operator_token(value=value[0], operator=operator, wildcard_symbol=wildcard_symbol)
            return [self._clean_value(value=v, wildcard_symbol=wildcard_symbol) for v in value], op

        op = self.__get_operator_token(value=value, operator=operator, wildcard_symbol=wildcard_symbol)
        return self._clean_value(value, wildcard_symbol), op

    @staticmethod
    def create_field(field_name: str, operator: Identifier, value: Union[str, List]) -> Field:
        return Field(operator=operator, value=value, source_name=field_name)

    def search_field_value(self, query):
        field_name = self.search_field(query)
        operator = self.search_match_operator(query, field_name)
        query, operator, value = self.search_value(query=query, operator=operator, field_name=field_name)
        value, operator_token = self.process_value_wildcard_symbols(value=value,
                                                                    operator=operator,
                                                                    wildcard_symbol=self.wildcard_symbol)
        field = self.create_field(field_name=field_name, operator=operator_token, value=value)
        return field, query

    def __get_identifier(self, query: str) -> Tuple[Union[Field, Keyword, Identifier], str]:
        query = query.strip("\n").strip(" ").strip("\n")
        if query.startswith(GroupType.L_PAREN):
            return Identifier(token_type=GroupType.L_PAREN), query[1:]
        elif query.startswith(GroupType.R_PAREN):
            return Identifier(token_type=GroupType.R_PAREN), query[1:]
        elif operator_search := re.match(self.operator_pattern, query):
            operator = operator_search.group("operator")
            pos = operator_search.end()
            return Identifier(token_type=operator.lower()), query[pos:]
        elif self.keyword_pattern and re.match(self.keyword_pattern, query):
            return self.search_keyword(query)
        else:
            return self.search_field_value(query)

    @staticmethod
    def _validate_parentheses(tokens):
        parentheses = []
        for token in tokens:
            if isinstance(token, Identifier) and token.token_type in (GroupType.L_PAREN, GroupType.R_PAREN):
                if token.token_type == GroupType.L_PAREN:
                    parentheses.append(token)
                elif not parentheses or parentheses[-1].token_type == GroupType.R_PAREN:
                    raise QueryParenthesesException()
                else:
                    parentheses.pop()
        if parentheses:
            raise QueryParenthesesException()
        return True

    def tokenize(self, query: str) -> List[Union[Field, Keyword, Identifier]]:
        tokenized = []
        while query:
            identifier, query = self.__get_identifier(query=query)
            tokenized.append(identifier)
        self._validate_parentheses(tokenized)
        return tokenized

    @staticmethod
    def filter_tokens(tokens: List[TOKEN_TYPE],
                      token_type: Union[Type[Field], Type[Keyword], Type[Identifier]]) -> List[TOKEN_TYPE]:
        return [token for token in tokens if isinstance(token, token_type)]

    def filter_function_tokens(self,
                               tokens: List[Union[Field, Keyword, Identifier, Function, SortArg]]) -> List[TOKEN_TYPE]:
        result = []
        for token in tokens:
            if isinstance(token, Field):
                result.append(token)
            elif isinstance(token, Function):
                result.extend(self.filter_function_tokens(tokens=token.args))
                result.extend(self.filter_function_tokens(tokens=token.by_clauses))
            elif isinstance(token, SortArg):
                result.append(token.field)
        return result

    @staticmethod
    def set_field_generic_names_map(tokens: List[Field],
                                    source_mappings: List[SourceMapping],
                                    platform_mappings: BasePlatformMappings) -> None:
        for token in tokens:
            generic_names_map = {
                source_mapping.source_id: source_mapping.fields_mapping.get_generic_field_name(token.source_name)
                for source_mapping in source_mappings
            }
            if DEFAULT_MAPPING_NAME not in generic_names_map:
                default_source_mapping = platform_mappings.get_source_mapping(DEFAULT_MAPPING_NAME)
                fields_mapping = default_source_mapping.fields_mapping
                generic_names_map[DEFAULT_MAPPING_NAME] = fields_mapping.get_generic_field_name(token.source_name)

            token.generic_names_map = generic_names_map
