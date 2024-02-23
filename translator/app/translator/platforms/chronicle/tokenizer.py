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

import re
from typing import Any, ClassVar

from app.translator.core.custom_types.tokens import OperatorType
from app.translator.core.custom_types.values import ValueType
from app.translator.core.exceptions.parser import TokenizerGeneralException
from app.translator.core.models.field import FieldValue
from app.translator.core.models.identifier import Identifier
from app.translator.core.tokenizer import QueryTokenizer
from app.translator.platforms.chronicle.escape_manager import chronicle_escape_manager
from app.translator.tools.utils import get_match_group


class ChronicleQueryTokenizer(QueryTokenizer):
    single_value_operators_map: ClassVar[dict[str, str]] = {
        "=": OperatorType.EQ,
        "<=": OperatorType.LTE,
        "<": OperatorType.LT,
        ">=": OperatorType.GTE,
        ">": OperatorType.GT,
        "!=": OperatorType.NEQ,
    }

    field_pattern = r"(?P<field_name>[a-zA-Z0-9\._]+)"
    num_value_pattern = rf"(?P<{ValueType.number_value}>\d+(?:\.\d+)*)\s*"
    bool_value_pattern = rf"(?P<{ValueType.bool_value}>true|false)\s*"
    double_quotes_value_pattern = rf'"(?P<{ValueType.double_quotes_value}>(?:[:a-zA-Z\*0-9=+%#\-_/,\'\.$&^@!\(\)\{{\}}\s]|\\\"|\\\\)*)"\s*(?:nocase)?'  # noqa: E501
    re_value_pattern = (
        rf"/(?P<{ValueType.regex_value}>(?:\\\/|[:a-zA-Z\*0-9=+%#\\\-_\,\"\'\.$&^@!\(\)\{{\}}\s?])+)/\s*(?:nocase)?"
    )
    _value_pattern = rf"{num_value_pattern}|{bool_value_pattern}|{double_quotes_value_pattern}|{re_value_pattern}"
    escape_manager = chronicle_escape_manager

    wildcard_symbol = ".*"

    def get_operator_and_value(self, match: re.Match, operator: str = OperatorType.EQ) -> tuple[str, Any]:
        if (num_value := get_match_group(match, group_name=ValueType.number_value)) is not None:
            return operator, num_value

        if (bool_value := get_match_group(match, group_name=ValueType.bool_value)) is not None:
            return operator, bool_value

        if (d_q_value := get_match_group(match, group_name=ValueType.double_quotes_value)) is not None:
            return operator, self.escape_manager.remove_escape(d_q_value)

        if (re_value := get_match_group(match, group_name=ValueType.regex_value)) is not None:
            return OperatorType.REGEX, re_value

        return super().get_operator_and_value(match, operator)

    def escape_field_name(self, field_name: str) -> str:
        symbols_to_check = [".", "_", "$"]
        for symbol in symbols_to_check:
            field_name = field_name.replace(symbol, "\\" + symbol)
        return field_name


class ChronicleRuleTokenizer(ChronicleQueryTokenizer):
    field_pattern = r"(?P<field_name>[$a-zA-Z0-9\._]+)"
    regex_field_regex = r"re\.regex\((?P<field>[$a-zA-Z\._]+),"

    double_quotes_value_pattern = (
        rf'"(?P<{ValueType.double_quotes_value}>(?:[:a-zA-Z\*0-9=+%#\-_/,\'\.$&^@!\(\)\{{\}}\s]|\\\"|\\\\)*)"'
    )
    back_quotes_value_pattern = (
        rf"`(?P<{ValueType.back_quotes_value}>(?:[:a-zA-Z\*0-9=+%#\-_/,\'\"\\\.$&^@!\(\)\{{\}}\s])*)`"
    )
    regex_value_regex = rf"{double_quotes_value_pattern}|{back_quotes_value_pattern}\s*\)\s*(?:nocase)?\s*"

    def search_field_value(self, query: str) -> tuple[FieldValue, str]:
        if query.startswith("re.regex("):
            field_search = re.search(self.regex_field_regex, query)
            if field_search is None:
                raise TokenizerGeneralException(error=f"Field couldn't be found in query part: {query}")

            field = field_search.group("field")
            pos = field_search.end()
            query = query[pos:]

            value_search = re.search(self.regex_value_regex, query)
            if value_search is None:
                raise TokenizerGeneralException(error=f"Value couldn't be found in query part: {query}")

            operator = OperatorType.REGEX
            operator, value = self.get_operator_and_value(value_search, operator)
            operator, value = self.process_value_wildcards(value=value, operator=OperatorType.REGEX)
            pos = value_search.end()
            query = query[pos:]

            operator_token = Identifier(token_type=operator)
            field_value = self.create_field_value(field_name=field, operator=operator_token, value=value)
            return field_value, query

        return super().search_field_value(query=query)

    def get_operator_and_value(self, match: re.Match, operator: str = OperatorType.EQ) -> tuple[str, Any]:
        if (d_q_value := get_match_group(match, group_name=ValueType.double_quotes_value)) is not None:
            return operator, self.escape_manager.remove_escape(d_q_value)

        if (b_q_value := get_match_group(match, group_name=ValueType.back_quotes_value)) is not None:
            return operator, self.escape_manager.remove_escape(b_q_value)

        return super().get_operator_and_value(match, operator)
