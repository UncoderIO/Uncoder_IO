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
from typing import Tuple, Any, List, Union

from app.translator.core.custom_types.values import ValueType
from app.translator.core.mixins.logic import ANDLogicOperatorMixin
from app.translator.core.models.field import Keyword, FieldValue
from app.translator.core.models.identifier import Identifier
from app.translator.core.custom_types.tokens import LogicalOperatorType, OperatorType
from app.translator.core.tokenizer import QueryTokenizer
from app.translator.platforms.logscale.escape_manager import logscale_escape_manager
from app.translator.tools.utils import get_match_group


class LogScaleTokenizer(QueryTokenizer, ANDLogicOperatorMixin):
    single_value_operators_map = {
        "=": OperatorType.EQ,
        "<=": OperatorType.LTE,
        "<": OperatorType.LT,
        ">=": OperatorType.GTE,
        ">": OperatorType.GT,
        "!=": OperatorType.NEQ
    }

    field_pattern = r"(?P<field_name>[a-zA-Z\._\-]+)"
    num_value_pattern = fr"(?P<{ValueType.number_value}>\d+(?:\.\d+)*)\s*"
    double_quotes_value_pattern = fr'"(?P<{ValueType.double_quotes_value}>(?:[:a-zA-Z\*0-9=+%#\-_/,\'\.$&^@!\(\)\{{\}}\s]|\\\"|\\)*)"\s*'
    re_value_pattern = fr"/(?P<{ValueType.regular_expression_value}>[:a-zA-Z\*0-9=+%#\\\-_\,\"\'\.$&^@!\(\)\{{\}}\s?]+)/i?\s*"
    _value_pattern = fr"""{num_value_pattern}|{re_value_pattern}|{double_quotes_value_pattern}"""
    keyword_pattern = double_quotes_value_pattern
    escape_manager = logscale_escape_manager
    wildcard_symbol = "*"

    def get_operator_and_value(self, match: re.Match, operator: str = OperatorType.EQ) -> Tuple[str, Any]:
        if (num_value := get_match_group(match, group_name=ValueType.number_value)) is not None:
            return operator, num_value

        elif (d_q_value := get_match_group(match, group_name=ValueType.double_quotes_value)) is not None:
            return operator, d_q_value

        elif (re_value := get_match_group(match, group_name=ValueType.regular_expression_value)) is not None:
            return OperatorType.REGEX, re_value

        return super().get_operator_and_value(match, operator)

    def _get_identifier(self, query: str) -> (list, str):
        query = query.strip("\n").strip(" ").strip("\n")
        if query.startswith('!'):
            return Identifier(token_type=LogicalOperatorType.NOT), query[1:]

        return super()._get_identifier(query)

    def tokenize(self, query: str) -> List[Union[FieldValue, Keyword, Identifier]]:
        tokens = super().tokenize(query=query)
        return self.add_and_token_if_missed(tokens=tokens)
