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
from typing import Any, ClassVar, Union

from app.translator.core.custom_types.tokens import OperatorType
from app.translator.core.custom_types.values import ValueType
from app.translator.core.mixins.logic import ANDLogicOperatorMixin
from app.translator.core.models.field import FieldValue, Keyword
from app.translator.core.models.identifier import Identifier
from app.translator.core.tokenizer import QueryTokenizer
from app.translator.platforms.base.spl.escape_manager import spl_escape_manager
from app.translator.tools.utils import get_match_group


class SplTokenizer(QueryTokenizer, ANDLogicOperatorMixin):
    single_value_operators_map: ClassVar[dict[str, str]] = {
        "=": OperatorType.EQ,
        "<=": OperatorType.LTE,
        "<": OperatorType.LT,
        ">=": OperatorType.GTE,
        ">": OperatorType.GT,
        "!=": OperatorType.NEQ,
    }
    multi_value_operators_map: ClassVar[dict[str, str]] = {"in": OperatorType.EQ}

    field_pattern = r"(?P<field_name>[a-zA-Z0-9\.\-_\{\}]+)"
    num_value_pattern = rf"(?P<{ValueType.number_value}>\d+(?:\.\d+)*)(?=$|\s|\))"
    double_quotes_value_pattern = rf'"(?P<{ValueType.double_quotes_value}>(?:[:a-zA-Z\*0-9=+%#\-_/,;`\?~‘○×\'\.<>$&^@!\]\[\(\)\{{\}}\s]|\\\"|\\)*)"\s*' # noqa
    single_quotes_value_pattern = (
        rf"'(?P<{ValueType.single_quotes_value}>(?:[:a-zA-Z\*0-9=+%#\-_/,;\"\.<>$&^@!\(\)\{{\}}\s]|\\\'|\\)*)'\s*"
    )
    no_quotes_value_pattern = rf"(?P<{ValueType.no_quotes_value}>(?:[:a-zA-Z\*0-9+%#\-_/,\.$&^@!]|\\\s|\\=|\\!=|\\<|\\<=|\\>|\\>=|\\\\)+)(?=$|\s|\))"  # noqa: E501
    _value_pattern = (
        rf"{num_value_pattern}|{no_quotes_value_pattern}|{double_quotes_value_pattern}|{single_quotes_value_pattern}"
    )
    multi_value_pattern = rf"""\((?P<{ValueType.value}>[:a-zA-Z\"\*0-9=+%#\-_\/\\'\,;.$&^@!\{{\}}\(\s]+)\)"""
    keyword_pattern = rf"{double_quotes_value_pattern}|{no_quotes_value_pattern}"

    wildcard_symbol = "*"

    escape_manager = spl_escape_manager

    def get_operator_and_value(self, match: re.Match, operator: str = OperatorType.EQ) -> tuple[str, Any]:
        if (num_value := get_match_group(match, group_name=ValueType.number_value)) is not None:
            return operator, num_value

        if (no_q_value := get_match_group(match, group_name=ValueType.no_quotes_value)) is not None:
            return operator, no_q_value

        if (d_q_value := get_match_group(match, group_name=ValueType.double_quotes_value)) is not None:
            return operator, self.escape_manager.remove_escape(d_q_value)

        if (s_q_value := get_match_group(match, group_name=ValueType.single_quotes_value)) is not None:
            return operator, self.escape_manager.remove_escape(s_q_value)

        return super().get_operator_and_value(match)

    def tokenize(self, query: str) -> list[Union[FieldValue, Keyword, Identifier]]:
        tokens = super().tokenize(query=query)
        return self.add_and_token_if_missed(tokens=tokens)
