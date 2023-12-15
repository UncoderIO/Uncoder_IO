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

from app.translator.core.mixins.logic import ANDLogicOperatorMixin
from app.translator.core.models.field import Field, Keyword
from app.translator.core.models.identifier import Identifier
from app.translator.core.tokenizer import QueryTokenizer
from app.translator.core.custom_types.tokens import OperatorType
from app.translator.tools.utils import get_match_group


class SplTokenizer(QueryTokenizer, ANDLogicOperatorMixin):
    single_value_operators_map = {
        "=": OperatorType.EQ,
        "<=": OperatorType.LTE,
        "<": OperatorType.LT,
        ">=": OperatorType.GTE,
        ">": OperatorType.GT,
        "!=": OperatorType.NEQ
    }
    multi_value_operators_map = {"in": OperatorType.EQ}

    field_pattern = r"(?P<field_name>[a-zA-Z\.\-_\{\}]+)"
    num_value_pattern = r"(?P<num_value>\d+(?:\.\d+)*)(?=$|\s|\))"
    double_quotes_value_pattern = r'"(?P<d_q_value>(?:[:a-zA-Z\*0-9=+%#\-_/,;\'\.$&^@!\]\[\(\)\{\}\s]|\\\"|\\)*)"\s*'
    single_quotes_value_pattern = r"'(?P<s_q_value>(?:[:a-zA-Z\*0-9=+%#\-_/,;\"\.$&^@!\(\)\{\}\s]|\\\'|\\)*)'\s*"
    no_quotes_value_pattern = r"(?P<no_q_value>(?:[:a-zA-Z\*0-9+%#\-_/,\.$&^@!]|\\\s|\\=|\\!=|\\<|\\<=|\\>|\\>=|\\\\)+)(?=$|\s|\))"
    _value_pattern = fr"{num_value_pattern}|{no_quotes_value_pattern}|{double_quotes_value_pattern}|{single_quotes_value_pattern}"
    multi_value_pattern = r"""\((?P<value>[:a-zA-Z\"\*0-9=+%#\-_\/\\'\,;.$&^@!\{\}\(\s]+)\)"""
    keyword_pattern = fr"{double_quotes_value_pattern}|{no_quotes_value_pattern}"

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

    def tokenize(self, query: str) -> List[Union[Field, Keyword, Identifier]]:
        tokens = super().tokenize(query=query)
        return self.add_and_token_if_missed(tokens=tokens)
