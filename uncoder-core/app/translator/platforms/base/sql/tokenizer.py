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
from typing import Any, ClassVar, Optional, Union

from app.translator.core.custom_types.tokens import OperatorType
from app.translator.core.custom_types.values import ValueType
from app.translator.core.models.query_tokens.field_value import FieldValue
from app.translator.core.models.query_tokens.function_value import FunctionValue
from app.translator.core.models.query_tokens.identifier import Identifier
from app.translator.core.models.query_tokens.keyword import Keyword
from app.translator.core.tokenizer import QueryTokenizer
from app.translator.platforms.base.sql.custom_types.values import SQLValueType
from app.translator.platforms.base.sql.str_value_manager import sql_str_value_manager
from app.translator.tools.utils import get_match_group

_ESCAPE_SYMBOL_GROUP_NAME = "escape_symbol"


class SQLTokenizer(QueryTokenizer):
    single_value_operators_map: ClassVar[dict[str, str]] = {
        "=": OperatorType.EQ,
        "<=": OperatorType.LTE,
        "<": OperatorType.LT,
        ">=": OperatorType.GTE,
        ">": OperatorType.GT,
        "!=": OperatorType.NOT_EQ,
        "<>": OperatorType.NOT_EQ,
        "like": OperatorType.EQ,
    }
    multi_value_operators_map: ClassVar[dict[str, str]] = {"in": OperatorType.EQ}

    field_pattern = r'(?P<field_name>"[a-zA-Z\._\-\s]+"|[a-zA-Z\._\-]+)'
    num_value_pattern = rf"(?P<{ValueType.number_value}>\d+(?:\.\d+)*)\s*"
    bool_value_pattern = rf"(?P<{ValueType.bool_value}>true|false)\s*"
    single_quotes_value_pattern = rf"""'(?P<{ValueType.single_quotes_value}>(?:[:a-zA-Z\*0-9=+%#\-\/,_".$&^@!\(\)\{{\}}\s]|''|\\\'|\\\%|\\\_|\\\\|\\)*)'(?:\s+escape\s+'(?P<{_ESCAPE_SYMBOL_GROUP_NAME}>.)')?"""  # noqa: E501
    _value_pattern = rf"{num_value_pattern}|{bool_value_pattern}|{single_quotes_value_pattern}"
    multi_value_pattern = rf"""\((?P<{ValueType.multi_value}>\d+(?:,\s*\d+)*|'(?:[:a-zA-Z\*0-9=+%#\-\/\\,_".$&^@!\(\)\{{\}}\s]|'')*'(?:,\s*'(?:[:a-zA-Z\*0-9=+%#\-\/\\,_".$&^@!\(\)\{{\}}\s]|'')*')*)\)"""  # noqa: E501
    re_field_value_pattern = rf"""regexp_like\({field_pattern},\s*'(?P<{ValueType.regex_value}>(?:[:a-zA-Z\*\?0-9=+%#№;\-_,"\.$&^@!\{{\}}\[\]\s?<>|]|\\\'|\\)+)'\)"""  # noqa: E501

    wildcard_symbol = "%"

    str_value_manager = sql_str_value_manager

    @staticmethod
    def should_process_value_wildcards(operator: Optional[str]) -> bool:
        return operator and operator.lower() in ("like",)

    def get_operator_and_value(
        self, match: re.Match, mapped_operator: str = OperatorType.EQ, operator: Optional[str] = None
    ) -> tuple[str, Any]:
        if (num_value := get_match_group(match, group_name=ValueType.number_value)) is not None:
            return mapped_operator, num_value

        if (bool_value := get_match_group(match, group_name=ValueType.bool_value)) is not None:
            mapped_bool_value = bool_value == "true"
            return mapped_operator, mapped_bool_value

        if (s_q_value := get_match_group(match, group_name=ValueType.single_quotes_value)) is not None:
            escape_symbol = get_match_group(match, group_name=_ESCAPE_SYMBOL_GROUP_NAME)
            should_process_value_wildcards = self.should_process_value_wildcards(operator)
            value_type = SQLValueType.like_value if should_process_value_wildcards else SQLValueType.value
            return mapped_operator, self.str_value_manager.from_str_to_container(
                s_q_value, value_type=value_type, escape_symbol=escape_symbol
            )

        return super().get_operator_and_value(match, mapped_operator, operator)

    @staticmethod
    def create_field_value(field_name: str, operator: Identifier, value: Union[str, list]) -> FieldValue:
        field_name = field_name.strip('"')
        return FieldValue(source_name=field_name, operator=operator, value=value)

    def _search_re_field_value(self, query: str) -> Optional[tuple[FieldValue, str]]:
        if match := re.match(self.re_field_value_pattern, query, re.IGNORECASE):
            group_dict = match.groupdict()
            field_name = group_dict["field_name"]
            value = self.str_value_manager.from_re_str_to_container(group_dict[ValueType.regex_value])
            operator = Identifier(token_type=OperatorType.REGEX)
            return self.create_field_value(field_name, operator, value), query[match.end() :]

    def _get_next_token(
        self, query: str
    ) -> tuple[Union[FieldValue, FunctionValue, Keyword, Identifier, list[Union[FieldValue, Identifier]]], str]:
        query = query.strip("\n").strip(" ").strip("\n")
        if search_result := self._search_re_field_value(query):
            return search_result
        return super()._get_next_token(query)
