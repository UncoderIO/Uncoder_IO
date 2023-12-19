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
from typing import Tuple, Any

from app.translator.core.exceptions.parser import TokenizerGeneralException
from app.translator.core.tokenizer import QueryTokenizer
from app.translator.core.custom_types.tokens import OperatorType
from app.translator.tools.utils import get_match_group


class ChronicleQueryTokenizer(QueryTokenizer):
    single_value_operators_map = {
        "=": OperatorType.EQ,
        "<=": OperatorType.LTE,
        "<": OperatorType.LT,
        ">=": OperatorType.GTE,
        ">": OperatorType.GT,
        "!=": OperatorType.NEQ
    }

    field_pattern = r"(?P<field_name>[a-zA-Z0-9\._]+)"
    num_value_pattern = r"(?P<num_value>\d+(?:\.\d+)*)\s*"
    bool_value_pattern = r"(?P<bool_value>true|false)\s*"
    double_quotes_value_pattern = r'"(?P<d_q_value>(?:[:a-zA-Z\*0-9=+%#\-_/,\'\.$&^@!\(\)\{\}\s]|\\\"|\\\\)*)"\s*(?:nocase)?'
    re_value_pattern = r"/(?P<re_value>(?:\\\/|[:a-zA-Z\*0-9=+%#\\\-_\,\"\'\.$&^@!\(\)\{\}\s?])+)/\s*(?:nocase)?"
    _value_pattern = fr"{num_value_pattern}|{bool_value_pattern}|{double_quotes_value_pattern}|{re_value_pattern}"

    wildcard_symbol = ".*"

    def get_operator_and_value(self, match: re.Match, operator: str = OperatorType.EQ) -> Tuple[str, Any]:
        if (num_value := get_match_group(match, group_name='num_value')) is not None:
            return operator, num_value

        elif (bool_value := get_match_group(match, group_name='bool_value')) is not None:
            return operator, bool_value

        elif (d_q_value := get_match_group(match, group_name='d_q_value')) is not None:
            return operator, d_q_value

        elif (re_value := get_match_group(match, group_name='re_value')) is not None:
            return OperatorType.REGEX, re_value

        return super().get_operator_and_value(match, operator)

    def escape_field_name(self, field_name):
        symbols_to_check = [".", "_", "$"]
        for symbol in symbols_to_check:
            field_name = field_name.replace(symbol, '\\' + symbol)
        return field_name


class ChronicleRuleTokenizer(ChronicleQueryTokenizer):
    field_pattern = r"(?P<field_name>[$a-zA-Z0-9\._]+)"
    regex_field_regex = r"re\.regex\((?P<field>[$a-zA-Z\._]+),"

    double_quotes_value_pattern = r'"(?P<d_q_value>(?:[:a-zA-Z\*0-9=+%#\-_/,\'\.$&^@!\(\)\{\}\s]|\\\"|\\\\)*)"'
    back_quotes_value_pattern = r'`(?P<b_q_value>(?:[:a-zA-Z\*0-9=+%#\-_/,\'\"\\\.$&^@!\(\)\{\}\s])*)`'
    regex_value_regex = fr"{double_quotes_value_pattern}|{back_quotes_value_pattern}\s*\)\s*(?:nocase)?\s*"

    def search_field_value(self, query):
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
            value, operator = self.process_value_wildcard_symbols(
                value=value, operator=OperatorType.REGEX, wildcard_symbol=self.wildcard_symbol
            )
            pos = value_search.end()
            query = query[pos:]

            field = self.create_field(field_name=field, operator=operator, value=value)
            return field, query
        else:
            return super().search_field_value(query=query)

    def get_operator_and_value(self, match: re.Match, operator: str = OperatorType.EQ) -> Tuple[str, Any]:
        if (d_q_value := get_match_group(match, group_name='d_q_value')) is not None:
            return operator, d_q_value

        elif (b_q_value := get_match_group(match, group_name='b_q_value')) is not None:
            return operator, b_q_value

        return super().get_operator_and_value(match, operator)
