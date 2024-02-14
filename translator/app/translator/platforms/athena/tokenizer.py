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
from app.translator.core.models.field import FieldValue
from app.translator.core.models.identifier import Identifier
from app.translator.core.tokenizer import QueryTokenizer
from app.translator.tools.utils import get_match_group


class AthenaTokenizer(QueryTokenizer):
    single_value_operators_map: ClassVar[dict[str, str]] = {
        "=": OperatorType.EQ,
        "<=": OperatorType.LTE,
        "<": OperatorType.LT,
        ">=": OperatorType.GTE,
        ">": OperatorType.GT,
        "!=": OperatorType.NEQ,
        "<>": OperatorType.NEQ,
        "like": OperatorType.EQ,
    }
    multi_value_operators_map: ClassVar[dict[str, str]] = {"in": OperatorType.EQ}

    field_pattern = r'(?P<field_name>"[a-zA-Z\._\-\s]+"|[a-zA-Z\._\-]+)'
    num_value_pattern = rf"(?P<{ValueType.number_value}>\d+(?:\.\d+)*)\s*"
    bool_value_pattern = rf"(?P<{ValueType.bool_value}>true|false)\s*"
    single_quotes_value_pattern = (
        rf"""'(?P<{ValueType.single_quotes_value}>(?:[:a-zA-Z\*0-9=+%#\-\/\\,_".$&^@!\(\)\{{\}}\s]|'')*)'"""
    )
    _value_pattern = rf"{num_value_pattern}|{bool_value_pattern}|{single_quotes_value_pattern}"
    multi_value_pattern = rf"""\((?P<{ValueType.value}>\d+(?:,\s*\d+)*|'(?:[:a-zA-Z\*0-9=+%#\-\/\\,_".$&^@!\(\)\{{\}}\s]|'')*'(?:,\s*'(?:[:a-zA-Z\*0-9=+%#\-\/\\,_".$&^@!\(\)\{{\}}\s]|'')*')*)\)"""  # noqa: E501

    wildcard_symbol = "%"

    @staticmethod
    def should_process_value_wildcards(operator: str) -> bool:
        return operator.lower() in ("like",)

    def get_operator_and_value(self, match: re.Match, operator: str = OperatorType.EQ) -> tuple[str, Any]:
        if (num_value := get_match_group(match, group_name=ValueType.number_value)) is not None:
            return operator, num_value

        if (bool_value := get_match_group(match, group_name=ValueType.bool_value)) is not None:
            return operator, bool_value

        if (s_q_value := get_match_group(match, group_name=ValueType.single_quotes_value)) is not None:
            return operator, s_q_value

        return super().get_operator_and_value(match, operator)

    @staticmethod
    def create_field_value(field_name: str, operator: Identifier, value: Union[str, list]) -> FieldValue:
        field_name = field_name.strip('"')
        return FieldValue(source_name=field_name, operator=operator, value=value)

    def tokenize(self, query: str) -> list:
        query = re.sub(r"\s*ESCAPE\s*'.'", "", query)  # remove `ESCAPE 'escape_char'` in LIKE expr
        return super().tokenize(query)
