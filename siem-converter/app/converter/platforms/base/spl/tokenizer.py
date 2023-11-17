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

from app.converter.core.tokenizer import QueryTokenizer
from app.converter.core.operator_types.tokens import OperatorType
from app.converter.tools.utils import get_match_group


class SplTokenizer(QueryTokenizer):
    field_pattern = r"(?P<field_name>[a-zA-Z\.\-_\{\}]+)"
    num_value_pattern = r"(?P<num_value>\d+(?:\.\d+)*)\s*"
    double_quotes_value_pattern = r'"(?P<d_q_value>(?:[:a-zA-Z\*0-9=+%#\-_/,;\'\.$&^@!\(\)\{\}\s]|\\\"|\\)*)"\s*'
    single_quotes_value_pattern = r"'(?P<s_q_value>(?:[:a-zA-Z\*0-9=+%#\-_/,;\"\.$&^@!\(\)\{\}\s]|\\\'|\\)*)'\s*"
    no_quotes_value = r"(?P<no_q_value>(?:[:a-zA-Z\*0-9=+%#\-_/,\.\\$&^@!])+)\s*"
    _value_pattern = fr"{num_value_pattern}|{no_quotes_value}|{double_quotes_value_pattern}|{single_quotes_value_pattern}"
    multi_value_pattern = r"""\((?P<value>[:a-zA-Z\"\*0-9=+%#\-_\/\\'\,;.$&^@!\{\}\(\s]+)\)"""
    keyword_pattern = double_quotes_value_pattern

    multi_value_operators = ("in",)
    wildcard_symbol = "*"

    def get_operator_and_value(self, match: re.Match, operator: str = OperatorType.EQ) -> Tuple[str, Any]:
        if (num_value := get_match_group(match, group_name='num_value')) is not None:
            return operator, num_value

        elif (no_q_value := get_match_group(match, group_name='no_q_value')) is not None:
            return operator, no_q_value

        elif (d_q_value := get_match_group(match, group_name='d_q_value')) is not None:
            return operator, d_q_value

        elif (s_q_value := get_match_group(match, group_name='s_q_value')) is not None:
            return operator, s_q_value

        return super().get_operator_and_value(match)
