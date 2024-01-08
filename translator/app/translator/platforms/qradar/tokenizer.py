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

from app.translator.core.custom_types.values import ValueType
from app.translator.platforms.qradar.const import UTF8_PAYLOAD_PATTERN, SINGLE_QUOTES_VALUE_PATTERN, NUM_VALUE_PATTERN
from app.translator.core.models.field import Keyword, FieldValue
from app.translator.core.models.identifier import Identifier
from app.translator.core.tokenizer import QueryTokenizer
from app.translator.core.custom_types.tokens import OperatorType
from app.translator.platforms.qradar.escape_manager import qradar_escape_manager
from app.translator.tools.utils import get_match_group


class QradarTokenizer(QueryTokenizer):

    single_value_operators_map = {
        "=": OperatorType.EQ,
        "<=": OperatorType.LTE,
        "<": OperatorType.LT,
        ">=": OperatorType.GTE,
        ">": OperatorType.GT,
        "!=": OperatorType.NEQ,
        "like": OperatorType.EQ,
        "ilike": OperatorType.EQ,
        "matches": OperatorType.REGEX,
        "imatches": OperatorType.REGEX
    }
    multi_value_operators_map = {
        "in": OperatorType.EQ
    }

    field_pattern = r'(?P<field_name>"[a-zA-Z\._\-\s]+"|[a-zA-Z\._\-]+)'
    bool_value_pattern = fr"(?P<{ValueType.bool_value}>true|false)\s*"
    _value_pattern = fr"{NUM_VALUE_PATTERN}|{bool_value_pattern}|{SINGLE_QUOTES_VALUE_PATTERN}"
    multi_value_pattern = fr"""\((?P<{ValueType.value}>[:a-zA-Z\"\*0-9=+%#\-_\/\\'\,.&^@!\(\s]*)\)"""
    keyword_pattern = fr"{UTF8_PAYLOAD_PATTERN}\s+(?:like|LIKE|ilike|ILIKE)\s+{SINGLE_QUOTES_VALUE_PATTERN}"
    escape_manager = qradar_escape_manager

    wildcard_symbol = "%"

    @staticmethod
    def should_process_value_wildcard_symbols(operator: str) -> bool:
        return operator.lower() in ("like", "ilike")

    def get_operator_and_value(self, match: re.Match, operator: str = OperatorType.EQ) -> Tuple[str, Any]:
        if (num_value := get_match_group(match, group_name=ValueType.number_value)) is not None:
            return operator, num_value

        elif (bool_value := get_match_group(match, group_name=ValueType.bool_value)) is not None:
            return operator, self.escape_manager.remove_escape(bool_value)

        elif (s_q_value := get_match_group(match, group_name=ValueType.single_quotes_value)) is not None:
            return operator, self.escape_manager.remove_escape(s_q_value)

        return super().get_operator_and_value(match, operator)

    def escape_field_name(self, field_name):
        field_name = field_name.replace('"', r'\"')
        field_name = field_name.replace(' ', r'\ ')
        return field_name

    def search_field_value(self, query) -> Tuple[FieldValue, str]:
        field_name = self.search_field(query)
        operator = self.search_operator(query, field_name)
        should_process_value_wildcard_symbols = self.should_process_value_wildcard_symbols(operator)
        query, operator, value = self.search_value(query=query, operator=operator, field_name=field_name)

        operator_token = Identifier(token_type=operator)
        if should_process_value_wildcard_symbols:
            value, operator_token = self.process_value_wildcard_symbols(
                value=value,
                operator=operator,
                wildcard_symbol=self.wildcard_symbol
            )

        field_name = field_name.strip('"')
        field_value = self.create_field_value(field_name=field_name, operator=operator_token, value=value)
        return field_value, query

    def search_keyword(self, query: str) -> Tuple[Keyword, str]:
        keyword_search = re.search(self.keyword_pattern, query)
        _, value = self.get_operator_and_value(keyword_search)
        keyword = Keyword(value=self._clean_value(value, self.wildcard_symbol))
        pos = keyword_search.end()
        return keyword, query[pos:]
