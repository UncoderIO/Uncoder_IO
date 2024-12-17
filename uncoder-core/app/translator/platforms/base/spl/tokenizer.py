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

from app.translator.core.const import QUERY_TOKEN_TYPE
from app.translator.core.custom_types.tokens import OperatorType
from app.translator.core.custom_types.values import ValueType
from app.translator.core.mixins.logic import ANDLogicOperatorMixin
from app.translator.core.tokenizer import QueryTokenizer
from app.translator.platforms.base.spl.const import DOUBLE_QUOTES_VALUE_PATTERN as D_Q_V_PATTERN
from app.translator.platforms.base.spl.const import FIELD_PATTERN
from app.translator.platforms.base.spl.const import NO_QUOTES_VALUES_PATTERN as NO_Q_V_PATTERN
from app.translator.platforms.base.spl.const import NUM_VALUE_PATTERN as N_V_PATTERN
from app.translator.platforms.base.spl.const import SINGLE_QUOTES_VALUE_PATTERN as S_Q_V_PATTERN
from app.translator.platforms.base.spl.str_value_manager import spl_str_value_manager
from app.translator.tools.utils import get_match_group


class SPLTokenizer(QueryTokenizer, ANDLogicOperatorMixin):
    single_value_operators_map: ClassVar[dict[str, str]] = {
        "=": OperatorType.EQ,
        "<=": OperatorType.LTE,
        "<": OperatorType.LT,
        ">=": OperatorType.GTE,
        ">": OperatorType.GT,
        "!=": OperatorType.NOT_EQ,
    }
    multi_value_operators_map: ClassVar[dict[str, str]] = {"in": OperatorType.EQ}

    field_pattern = FIELD_PATTERN.replace("___group_name___", "field_name")
    num_value_pattern = rf"{N_V_PATTERN.replace('___group_name___', ValueType.number_value)}(?=$|\s|\))"
    double_quotes_value_pattern = rf"{D_Q_V_PATTERN.replace('___group_name___', ValueType.double_quotes_value)}\s*"
    single_quotes_value_pattern = rf"{S_Q_V_PATTERN.replace('___group_name___', ValueType.single_quotes_value)}\s*"
    no_quotes_value_pattern = rf"{NO_Q_V_PATTERN.replace('___group_name___', ValueType.no_quotes_value)}(?=$|\s|\))"
    _value_pattern = (
        rf"{num_value_pattern}|{no_quotes_value_pattern}|{double_quotes_value_pattern}|{single_quotes_value_pattern}"
    )
    multi_value_pattern = rf"""\((?P<{ValueType.multi_value}>[:a-zA-Z\"\*0-9=+%#\-_\/\\'\,;.$&^@!\{{\}}\(\s]+)\)"""
    keyword_pattern = rf"{double_quotes_value_pattern}|{no_quotes_value_pattern}"

    wildcard_symbol = "*"

    str_value_manager = spl_str_value_manager

    def get_operator_and_value(
        self, match: re.Match, mapped_operator: str = OperatorType.EQ, operator: Optional[str] = None
    ) -> tuple[str, Any]:
        if (num_value := get_match_group(match, group_name=ValueType.number_value)) is not None:
            return mapped_operator, num_value

        if (no_q_value := get_match_group(match, group_name=ValueType.no_quotes_value)) is not None:
            return mapped_operator, self.str_value_manager.from_str_to_container(no_q_value)

        if (d_q_value := get_match_group(match, group_name=ValueType.double_quotes_value)) is not None:
            return mapped_operator, self.str_value_manager.from_str_to_container(d_q_value)

        if (s_q_value := get_match_group(match, group_name=ValueType.single_quotes_value)) is not None:
            return mapped_operator, self.str_value_manager.from_str_to_container(s_q_value)

        return super().get_operator_and_value(match, mapped_operator, operator)

    def tokenize(self, query: str) -> list[QUERY_TOKEN_TYPE]:
        tokens = super().tokenize(query=query)
        return self.add_and_token_if_missed(tokens=tokens)
