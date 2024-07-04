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
from typing import ClassVar, Optional, Union

from app.translator.core.custom_types.tokens import OperatorType
from app.translator.core.custom_types.values import ValueType
from app.translator.core.functions import PlatformFunctions
from app.translator.core.models.field import FieldValue, Keyword
from app.translator.core.models.function_value import FunctionValue
from app.translator.core.models.functions.base import Function
from app.translator.core.models.identifier import Identifier
from app.translator.core.str_value_manager import StrValue
from app.translator.core.tokenizer import QueryTokenizer
from app.translator.platforms.base.aql.const import NUM_VALUE_PATTERN, SINGLE_QUOTES_VALUE_PATTERN, UTF8_PAYLOAD_PATTERN
from app.translator.platforms.base.aql.functions.const import AQLFunctionGroupType
from app.translator.platforms.base.aql.str_value_manager import aql_str_value_manager
from app.translator.tools.utils import get_match_group


class AQLTokenizer(QueryTokenizer):
    single_value_operators_map: ClassVar[dict[str, str]] = {
        "=": OperatorType.EQ,
        "<=": OperatorType.LTE,
        "<": OperatorType.LT,
        ">=": OperatorType.GTE,
        ">": OperatorType.GT,
        "!=": OperatorType.NOT_EQ,
        "like": OperatorType.EQ,
        "ilike": OperatorType.EQ,
        "matches": OperatorType.REGEX,
        "imatches": OperatorType.REGEX,
    }
    multi_value_operators_map: ClassVar[dict[str, str]] = {"in": OperatorType.EQ}

    field_pattern = r'(?P<field_name>"[a-zA-Z\._\-\s]+"|[a-zA-Z\._\-]+)'
    function_pattern = r'(?P<func_name>[a-zA-Z_]+)\((?:(?:[a-zA-Z\._\-\s]+)|(?:"[a-zA-Z\._\-]+"))\)'
    bool_value_pattern = rf"(?P<{ValueType.bool_value}>true|false)\s*"
    _value_pattern = rf"{NUM_VALUE_PATTERN}|{bool_value_pattern}|{SINGLE_QUOTES_VALUE_PATTERN}"
    multi_value_pattern = rf"""\((?P<{ValueType.multi_value}>[:a-zA-Z\"\*0-9=+%#\-_\/\\'\,.&^@!\(\s]*)\)"""
    keyword_pattern = rf"{UTF8_PAYLOAD_PATTERN}\s+(?:like|LIKE|ilike|ILIKE)\s+{SINGLE_QUOTES_VALUE_PATTERN}"

    wildcard_symbol = "%"
    str_value_manager = aql_str_value_manager

    def __init__(self, platform_functions: PlatformFunctions = None):
        self.platform_functions = platform_functions

    @staticmethod
    def should_process_value_wildcards(operator: Optional[str]) -> bool:
        return operator and operator.lower() in ("like", "ilike")

    def get_operator_and_value(
        self, match: re.Match, mapped_operator: str = OperatorType.EQ, operator: Optional[str] = None
    ) -> tuple[str, StrValue]:
        if (num_value := get_match_group(match, group_name=ValueType.number_value)) is not None:
            return mapped_operator, StrValue(num_value, split_value=[num_value])

        if (bool_value := get_match_group(match, group_name=ValueType.bool_value)) is not None:
            return mapped_operator, StrValue(bool_value, split_value=[bool_value])

        if (s_q_value := get_match_group(match, group_name=ValueType.single_quotes_value)) is not None:
            if mapped_operator == OperatorType.REGEX:
                return mapped_operator, self.str_value_manager.from_re_str_to_container(s_q_value)

            if self.should_process_value_wildcards(operator):
                return mapped_operator, self.str_value_manager.from_str_to_container(s_q_value)

            return mapped_operator, self.str_value_manager.from_str_to_container(s_q_value)

        return super().get_operator_and_value(match, mapped_operator, operator)

    def escape_field_name(self, field_name: str) -> str:
        return field_name.replace('"', r"\"").replace(" ", r"\ ").replace("(", "\(").replace(")", "\)")

    @staticmethod
    def create_field_value(field_name: str, operator: Identifier, value: Union[str, list]) -> FieldValue:
        field_name = field_name.strip('"')
        return FieldValue(source_name=field_name, operator=operator, value=value)

    def search_keyword(self, query: str) -> tuple[Keyword, str]:
        keyword_search = re.search(self.keyword_pattern, query)
        _, value = self.get_operator_and_value(keyword_search)
        keyword = Keyword(value=value.strip(self.wildcard_symbol))
        pos = keyword_search.end()
        return keyword, query[pos:]

    def _search_function_value(self, function: Function, query: str) -> tuple[FunctionValue, str]:
        operator = self.search_operator(query, function.raw)
        if self.is_multi_value_flow(function.raw, operator, query):
            query, grouped_values = self.search_multi_value(query=query, operator=operator, field_name=function.raw)
            tokens = [  # always consists of 1 element
                FunctionValue(function=function, operator=Identifier(token_type=op), value=values)
                for op, values in grouped_values.items()
            ]
            return tokens[0], query

        query, operator, value = self.search_single_value(query=query, operator=operator, field_name=function.raw)
        operator_token = Identifier(token_type=operator)
        return FunctionValue(function=function, operator=operator_token, value=value), query

    def search_function_value(self, query: str) -> tuple[FunctionValue, str]:
        str_conversion_func_parser = self.platform_functions.manager.get_parser(AQLFunctionGroupType.str_conversion)
        if str_conversion_func_parser and (func_match := str_conversion_func_parser.get_func_match(query)):
            function = str_conversion_func_parser.parse(func_match.name, func_match.match)
            return self._search_function_value(function, query)

        return super().search_function_value(query)

    def _check_function_value_match(self, query: str, white_space_pattern: str = r"\s+") -> bool:
        single_value_operator_group = rf"(?:{'|'.join(self.single_value_operators_map)})"
        single_value_pattern = rf"""{self.function_pattern}\s*{single_value_operator_group}\s*{self.value_pattern}\s*"""
        if re.match(single_value_pattern, query, re.IGNORECASE):
            return True

        if self.multi_value_operators_map:
            multi_value_operator_group = rf"(?:{'|'.join(self.multi_value_operators_map)})"
            pattern = f"{self.function_pattern}{white_space_pattern}{multi_value_operator_group}{white_space_pattern}"
            multi_value_pattern = rf"{pattern}{self.multi_value_pattern}"
            if re.match(multi_value_pattern, query, re.IGNORECASE):
                return True

        return False
