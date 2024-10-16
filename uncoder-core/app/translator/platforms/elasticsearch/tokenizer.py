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
from app.translator.core.models.query_tokens.identifier import Identifier
from app.translator.core.tokenizer import QueryTokenizer
from app.translator.platforms.base.lucene.tokenizer import LuceneTokenizer
from app.translator.platforms.elasticsearch.str_value_manager import eql_str_value_manager
from app.translator.tools.utils import get_match_group


class ElasticSearchTokenizer(LuceneTokenizer):
    pass


class ElasticSearchEQLTokenizer(QueryTokenizer):
    single_value_operators_map: ClassVar[dict[str, str]] = {
        ":": OperatorType.EQ,
        "==": OperatorType.EQ,
        "<=": OperatorType.LTE,
        "<": OperatorType.LT,
        ">=": OperatorType.GTE,
        ">": OperatorType.GT,
        "!=": OperatorType.NOT_EQ,
        "regex~": OperatorType.REGEX,
        "regex": OperatorType.REGEX,
    }

    multi_value_operators_map: ClassVar[dict[str, str]] = {
        "in": OperatorType.EQ,
        "in~": OperatorType.EQ,
        ":": OperatorType.EQ,
    }
    wildcard_symbol = "*"
    field_pattern = r"(?P<field_name>[a-zA-Z\.\-_`]+)"
    re_value_pattern = (
        rf'"(?P<{ValueType.regex_value}>(?:[:a-zA-Z*0-9=+%#\-_/,;`?~‘\'.<>$&^@!\]\[()\s]|\\\"|\\)*)\[\^[z|Z]\]\.\?"'  # noqa: RUF001
    )
    double_quotes_value_pattern = (
        rf'"(?P<{ValueType.double_quotes_value}>(?:[:a-zA-Z*0-9=+%#\-_/,;`?~‘\'.<>$&^@!\]\[()\s]|\\\"|\\)*)"'  # noqa: RUF001
    )
    _value_pattern = rf"{re_value_pattern}|{double_quotes_value_pattern}"
    multi_value_pattern = rf"""\((?P<{ValueType.multi_value}>[:a-zA-Z\"\*0-9=+%#№;\-_\/\\'\,.$&^@!\(\[\]\s|]+)\)"""
    multi_value_check_pattern = r"___field___\s*___operator___\s*\("
    keyword_pattern = (
        rf'"(?P<{ValueType.double_quotes_value}>(?:[:a-zA-Z*0-9=+%#\-_/,;`?~‘\'.<>$&^@!\]\[()\s]|\\\"|\\)*)"'  # noqa: RUF001
    )

    str_value_manager = eql_str_value_manager

    def get_operator_and_value(
        self, match: re.Match, mapped_operator: str = OperatorType.EQ, operator: Optional[str] = None
    ) -> tuple[str, Any]:
        if (re_value := get_match_group(match, group_name=ValueType.regex_value)) is not None:
            return OperatorType.REGEX, self.str_value_manager.from_re_str_to_container(re_value)

        if (d_q_value := get_match_group(match, group_name=ValueType.double_quotes_value)) is not None:
            return mapped_operator, self.str_value_manager.from_str_to_container(d_q_value)

        return super().get_operator_and_value(match, mapped_operator, operator)

    def is_multi_value_flow(self, field_name: str, operator: str, query: str) -> bool:
        check_pattern = self.multi_value_check_pattern
        check_regex = check_pattern.replace("___field___", field_name).replace("___operator___", operator)
        return bool(re.match(check_regex, query))

    @staticmethod
    def create_field_value(field_name: str, operator: Identifier, value: Union[str, list]) -> FieldValue:
        field_name = field_name.replace("`", "")
        return FieldValue(source_name=field_name, operator=operator, value=value)
