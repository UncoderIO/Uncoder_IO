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
from typing import Tuple, Any, Union

from app.translator.core.mixins.operator import OperatorBasedMixin
from app.translator.core.tokenizer import QueryTokenizer
from app.translator.core.custom_types.tokens import OperatorType
from app.translator.tools.utils import get_match_group


class MicrosoftSentinelTokenizer(QueryTokenizer, OperatorBasedMixin):
    single_value_operators_map = {
        "==": OperatorType.EQ,
        "=~": OperatorType.EQ,
        "<=": OperatorType.LTE,
        "<": OperatorType.LT,
        ">=": OperatorType.GTE,
        ">": OperatorType.GT,
        "!=": OperatorType.NEQ,
        "!~": OperatorType.NEQ,
        "contains": OperatorType.CONTAINS,
        "startswith": OperatorType.STARTSWITH,
        "endswith": OperatorType.ENDSWITH,
    }
    multi_value_operators_map = {
        "in~": OperatorType.EQ,
        "in": OperatorType.EQ,
    }

    field_pattern = r"(?P<field_name>[a-zA-Z\.\-_]+)"
    bool_value_pattern = r"(?P<bool_value>true|false)\s*"
    num_value_pattern = r"(?P<num_value>\d+(?:\.\d+)*)\s*"
    double_quotes_value_pattern = r'@?"(?P<d_q_value>(?:[:a-zA-Z\*0-9=+%#\-_/,\'\.$&^@!\(\)\{\}\s]|\\\"|\\\\)*)"\s*'
    single_quotes_value_pattern = r"@?'(?P<s_q_value>(?:[:a-zA-Z\*0-9=+%#\-_/,\"\.$&^@!\(\)\{\}\s]|\\\'|\\\\)*)'\s*"
    str_value_pattern = fr"""{double_quotes_value_pattern}|{single_quotes_value_pattern}"""
    _value_pattern = fr"""{bool_value_pattern}|{num_value_pattern}|{str_value_pattern}"""
    multi_value_pattern = r"""\((?P<value>[:a-zA-Z\"\*0-9=+%#\-_\/\\'\,.&^@!\(\s]+)\)"""
    keyword_pattern = fr"\*\s+contains\s+(?:{str_value_pattern})"

    def get_operator_and_value(self, match: re.Match, operator: str = OperatorType.EQ) -> Tuple[str, Any]:
        if (num_value := get_match_group(match, group_name='num_value')) is not None:
            return operator, num_value

        elif (bool_value := get_match_group(match, group_name='bool_value')) is not None:
            return operator, bool_value

        elif (d_q_value := get_match_group(match, group_name='d_q_value')) is not None:
            return operator, d_q_value

        elif (s_q_value := get_match_group(match, group_name='s_q_value')) is not None:
            return operator, s_q_value

        return super().get_operator_and_value(match, operator)

    def clean_multi_value(self, value: Union[int, str]) -> Union[int, str]:
        if isinstance(value, str):
            value = value.strip(" ")
            value = value.lstrip("@")
            if value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            elif value.startswith('"') and value.endswith('"'):
                value = value[1:-1]

        return value
