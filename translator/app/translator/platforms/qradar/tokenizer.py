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

from app.translator.platforms.qradar.const import UTF8_PAYLOAD_PATTERN, SINGLE_QUOTES_VALUE_PATTERN, NUM_VALUE_PATTERN
from app.translator.core.models.field import Keyword
from app.translator.core.models.identifier import Identifier
from app.translator.core.tokenizer import QueryTokenizer
from app.translator.core.custom_types.tokens import OperatorType
from app.translator.tools.utils import get_match_group


class QradarTokenizer(QueryTokenizer):
    field_pattern = r'(?P<field_name>"[a-zA-Z\._\-\s]+"|[a-zA-Z\._\-]+)'
    match_operator_pattern = r"""(?:___field___\s?(?P<match_operator>like|ilike|matches|imatches|in|!=|>=|>|<=|<|=))\s?"""
    bool_value_pattern = r"(?P<bool_value>true|false)\s*"
    _value_pattern = fr"{NUM_VALUE_PATTERN}|{bool_value_pattern}|{SINGLE_QUOTES_VALUE_PATTERN}"
    keyword_pattern = fr"{UTF8_PAYLOAD_PATTERN}\s+(?:like|LIKE|ilike|ILIKE)\s+{SINGLE_QUOTES_VALUE_PATTERN}"

    multi_value_operators = ("in",)
    wildcard_symbol = "%"
    operators_map = {
        "like": OperatorType.EQ,
        "ilike": OperatorType.EQ,
        "matches": OperatorType.REGEX,
        "imatches": OperatorType.REGEX
    }

    def __init__(self):
        super().__init__()
        self.operators_map.update(super().operators_map)

    @staticmethod
    def should_process_value_wildcard_symbols(operator: str) -> bool:
        return operator.lower() in ("like", "ilike")

    def get_operator_and_value(self, match: re.Match, operator: str = OperatorType.EQ) -> Tuple[str, Any]:
        if (num_value := get_match_group(match, group_name='num_value')) is not None:
            return operator, num_value

        elif (bool_value := get_match_group(match, group_name='bool_value')) is not None:
            return operator, bool_value

        elif (s_q_value := get_match_group(match, group_name='s_q_value')) is not None:
            return operator, s_q_value

        return super().get_operator_and_value(match, operator)

    def escape_field_name(self, field_name):
        field_name = field_name.replace('"', r'\"')
        field_name = field_name.replace(' ', r'\ ')
        return field_name

    def search_field_value(self, query):
        field_name = self.search_field(query)
        operator = self.search_match_operator(query, field_name)
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
        field = self.create_field(field_name=field_name, operator=operator_token, value=value)
        return field, query

    def search_keyword(self, query: str) -> Tuple[Keyword, str]:
        keyword_search = re.search(self.keyword_pattern, query)
        _, value = self.get_operator_and_value(keyword_search)
        keyword = Keyword(value=self._clean_value(value, self.wildcard_symbol))
        pos = keyword_search.end()
        return keyword, query[pos:]
