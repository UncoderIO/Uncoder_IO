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
from typing import Any, ClassVar

from app.translator.core.custom_types.tokens import OperatorType
from app.translator.core.custom_types.values import ValueType
from app.translator.core.mixins.operator import OperatorBasedMixin
from app.translator.core.tokenizer import QueryTokenizer
from app.translator.platforms.microsoft.escape_manager import microsoft_escape_manager
from app.translator.tools.utils import get_match_group


class MicrosoftSentinelTokenizer(QueryTokenizer, OperatorBasedMixin):
    single_value_operators_map: ClassVar[dict[str, str]] = {
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
    multi_value_operators_map: ClassVar[dict[str, str]] = {"in~": OperatorType.EQ, "in": OperatorType.EQ}

    field_pattern = r"(?P<field_name>[a-zA-Z\.\-_]+)"
    bool_value_pattern = rf"(?P<{ValueType.bool_value}>true|false)\s*"
    num_value_pattern = rf"(?P<{ValueType.number_value}>\d+(?:\.\d+)*)\s*"
    double_quotes_value_pattern = (
        rf'(?P<{ValueType.double_quotes_value}>@?"(?:[:a-zA-Z\*0-9=+%#\-_/,\'\.$&^@!\(\)\{{\}}\s]|\\\"|\\\\)*")\s*'
    )
    single_quotes_value_pattern = (
        rf"(?P<{ValueType.single_quotes_value}>@?'(?:[:a-zA-Z\*0-9=+%#\-_/,\"\.$&^@!\(\)\{{\}}\s]|\\\'|\\\\)*')\s*"
    )
    str_value_pattern = rf"""{double_quotes_value_pattern}|{single_quotes_value_pattern}"""
    _value_pattern = rf"""{bool_value_pattern}|{num_value_pattern}|{str_value_pattern}"""
    multi_value_pattern = rf"""\((?P<{ValueType.multi_value}>[:a-zA-Z\"\*0-9=+%#\-_\/\\'\,.&^@!\(\s]+)\)"""
    keyword_pattern = rf"\*\s+contains\s+(?:{str_value_pattern})"

    escape_manager = microsoft_escape_manager

    def get_operator_and_value(self, match: re.Match, operator: str = OperatorType.EQ) -> tuple[str, Any]:  # noqa: PLR0911
        if (num_value := get_match_group(match, group_name=ValueType.number_value)) is not None:
            return operator, num_value

        if (bool_value := get_match_group(match, group_name=ValueType.bool_value)) is not None:
            return operator, bool_value

        if (d_q_value := get_match_group(match, group_name=ValueType.double_quotes_value)) is not None:
            if d_q_value.startswith("@"):
                return operator, d_q_value.lstrip("@").strip('"')
            return operator, self.escape_manager.remove_escape(d_q_value.strip('"'))

        if (s_q_value := get_match_group(match, group_name=ValueType.single_quotes_value)) is not None:
            if s_q_value.startswith("@"):
                return operator, s_q_value.lstrip("@").strip("'")
            return operator, self.escape_manager.remove_escape(s_q_value.strip("'"))

        return super().get_operator_and_value(match, operator)

    def clean_multi_value(self, value: str) -> str:
        value = value.strip(" ")
        value = value.lstrip("@")
        if value.startswith("'") and value.endswith("'") or value.startswith('"') and value.endswith('"'):
            value = value[1:-1]

        return value
