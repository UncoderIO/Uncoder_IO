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
from typing import Any, ClassVar, Optional

from app.translator.core.custom_types.tokens import OperatorType
from app.translator.core.mixins.operator import OperatorBasedMixin
from app.translator.core.str_value_manager import StrValue
from app.translator.core.tokenizer import QueryTokenizer
from app.translator.platforms.microsoft.custom_types.values import KQLValueType
from app.translator.platforms.microsoft.str_value_manager import microsoft_kql_str_value_manager
from app.translator.tools.utils import get_match_group


class MicrosoftSentinelTokenizer(QueryTokenizer, OperatorBasedMixin):
    single_value_operators_map: ClassVar[dict[str, str]] = {
        "==": OperatorType.EQ,
        "=~": OperatorType.EQ,
        "<=": OperatorType.LTE,
        "<": OperatorType.LT,
        ">=": OperatorType.GTE,
        ">": OperatorType.GT,
        "!=": OperatorType.NOT_EQ,
        "!~": OperatorType.NOT_EQ,
        "contains": OperatorType.CONTAINS,
        "startswith": OperatorType.STARTSWITH,
        "endswith": OperatorType.ENDSWITH,
        "matches regex": OperatorType.REGEX,
    }
    multi_value_operators_map: ClassVar[dict[str, str]] = {"in~": OperatorType.EQ, "in": OperatorType.EQ}

    field_pattern = r"(?P<field_name>[a-zA-Z\.\-_]+)"
    bool_value_pattern = rf"(?P<{KQLValueType.bool_value}>true|false)\s*"
    num_value_pattern = rf"(?P<{KQLValueType.number_value}>\d+(?:\.\d+)*)\s*"
    double_quotes_value_pattern = rf'"(?P<{KQLValueType.double_quotes_value}>(?:[:a-zA-Z\*0-9=+%#\-_/,\'\.$&^@!\(\)\{{\}}\[\];<>?`~\s]|\\\"|\\\\)*)"\s*'  # noqa: E501
    single_quotes_value_pattern = rf"'(?P<{KQLValueType.single_quotes_value}>(?:[:a-zA-Z\*0-9=+%#\-_/,\"\.$&^@!\(\)\{{\}}\[\];<>?`~\s]|\\\'|\\\\)*)'\s*"  # noqa: E501
    verbatim_double_quotes_value_pattern = rf'@"(?:\(i\?\))?(?P<{KQLValueType.verbatim_double_quotes_value}>(?:[:a-zA-Z\*0-9=+%#\-_/,\'\.$&^@!\(\)\{{\}}\[\];<>?`~\s\\]|"")*)"\s*'  # noqa: E501
    verbatim_single_quotes_value_pattern = rf"@'(?:\(i\?\))?(?P<{KQLValueType.verbatim_single_quotes_value}>(?:[:a-zA-Z\*0-9=+%#\-_/,\"\.$&^@!\(\)\{{\}}\[\];<>?`~\s\\]|'')*)'\s*"  # noqa: E501
    str_value_pattern = rf"""{double_quotes_value_pattern}|{single_quotes_value_pattern}|{verbatim_double_quotes_value_pattern}|{verbatim_single_quotes_value_pattern}"""  # noqa: E501
    _value_pattern = rf"""{bool_value_pattern}|{num_value_pattern}|{str_value_pattern}"""
    multi_value_pattern = rf"""\((?P<{KQLValueType.multi_value}>[:a-zA-Z\"\*0-9=+%#\-_\/\\'\,.&^@!\(\[\];<>?`~\s]+)\)"""
    keyword_pattern = rf"\*\s+contains\s+(?:{str_value_pattern})"

    str_value_manager = microsoft_kql_str_value_manager

    def get_operator_and_value(  # noqa: PLR0911
        self, match: re.Match, mapped_operator: str = OperatorType.EQ, operator: Optional[str] = None
    ) -> tuple[str, Any]:
        if (num_value := get_match_group(match, group_name=KQLValueType.number_value)) is not None:
            return mapped_operator, num_value

        if (bool_value := get_match_group(match, group_name=KQLValueType.bool_value)) is not None:
            mapped_bool_value = bool_value == "true"
            return mapped_operator, mapped_bool_value

        if (d_q_value := get_match_group(match, group_name=KQLValueType.double_quotes_value)) is not None:
            if mapped_operator == OperatorType.REGEX:
                value_type = KQLValueType.double_quotes_regex_value
                return mapped_operator, self.str_value_manager.from_re_str_to_container(d_q_value, value_type)
            return mapped_operator, self._str_to_container(d_q_value, KQLValueType.double_quotes_value)

        if (s_q_value := get_match_group(match, group_name=KQLValueType.single_quotes_value)) is not None:
            if mapped_operator == OperatorType.REGEX:
                value_type = KQLValueType.single_quotes_regex_value
                return mapped_operator, self.str_value_manager.from_re_str_to_container(s_q_value, value_type)
            return mapped_operator, self._str_to_container(s_q_value, KQLValueType.single_quotes_value)

        if (v_d_q_value := get_match_group(match, group_name=KQLValueType.verbatim_double_quotes_value)) is not None:
            if mapped_operator == OperatorType.REGEX:
                return mapped_operator, self.str_value_manager.from_re_str_to_container(v_d_q_value)
            return mapped_operator, self._str_to_container(v_d_q_value, KQLValueType.verbatim_double_quotes_value)

        if (v_s_q_value := get_match_group(match, group_name=KQLValueType.verbatim_single_quotes_value)) is not None:
            if mapped_operator == OperatorType.REGEX:
                return mapped_operator, self.str_value_manager.from_re_str_to_container(v_s_q_value)
            return mapped_operator, self._str_to_container(v_s_q_value, KQLValueType.verbatim_single_quotes_value)

        return super().get_operator_and_value(match, mapped_operator, operator)

    def _str_to_container(self, value: str, value_type: str) -> StrValue:
        return self.str_value_manager.from_str_to_container(value, value_type)

    def clean_multi_value(self, value: str) -> str:
        value = value.strip(" ")
        value = value.lstrip("@")
        if value.startswith("'") and value.endswith("'") or value.startswith('"') and value.endswith('"'):
            value = value[1:-1]

        return value
