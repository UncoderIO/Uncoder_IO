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
from typing import ClassVar, Union

from app.translator.core.custom_types.tokens import OperatorType
from app.translator.core.custom_types.values import ValueType
from app.translator.core.mixins.logic import ANDLogicOperatorMixin
from app.translator.core.models.field import FieldValue, Keyword
from app.translator.core.models.identifier import Identifier
from app.translator.core.str_value_manager import StrValue
from app.translator.core.tokenizer import QueryTokenizer
from app.translator.platforms.base.lucene.escape_manager import lucene_escape_manager
from app.translator.platforms.base.lucene.str_value_manager import lucene_str_value_manager
from app.translator.tools.utils import get_match_group


class LuceneTokenizer(QueryTokenizer, ANDLogicOperatorMixin):
    single_value_operators_map: ClassVar[dict[str, str]] = {
        ":>": OperatorType.GT,
        ":<": OperatorType.LT,
        ":": OperatorType.EQ,
    }
    multi_value_operators_map: ClassVar[dict[str, str]] = {":": OperatorType.EQ}

    field_pattern = r"(?P<field_name>[a-zA-Z\.\-_]+)"
    _num_value_pattern = r"\d+(?:\.\d+)?"
    num_value_pattern = rf"(?P<{ValueType.number_value}>{_num_value_pattern})(?=\s+|\)|$)"
    double_quotes_value_pattern = (
        rf'"(?P<{ValueType.double_quotes_value}>(?:[:a-zA-Z\*\?0-9=+%#№;\-_/,\'\.$&^@!\(\)\{{\}}\s]|\\\"|\\)*)"\s*'
    )
    no_quotes_value_pattern = (
        rf"(?P<{ValueType.no_quotes_value}>(?:[a-zA-Z\*\?0-9=%#№!;_/,\'\.$@|]|\\[*?\"-_=%#№!;,\.$@/\s\\])+)\s*"
    )
    re_value_pattern = rf"/(?P<{ValueType.regex_value}>(?:[:a-zA-Z\*\?0-9=+%#№;\\\-_\,\"\'\.$&^@!\(\)\{{\}}\[\]\s?<>|]|\\\/)+)/(?=\s+|\)|$)"  # noqa: E501
    gte_value_pattern = rf"\[\s*(?P<{ValueType.greater_than_or_equal}>{_num_value_pattern})\s+TO\s+\*\s*\]"
    lte_value_pattern = rf"\[\s*\*\s+TO\s+(?P<{ValueType.less_than_or_equal}>{_num_value_pattern})\s*\]"
    range_value_pattern = rf"{gte_value_pattern}|{lte_value_pattern}"
    _value_pattern = rf"{num_value_pattern}|{re_value_pattern}|{no_quotes_value_pattern}|{double_quotes_value_pattern}|{range_value_pattern}"  # noqa: E501
    keyword_pattern = (
        rf"(?P<{ValueType.no_quotes_value}>(?:[a-zA-Z\*\?0-9=%#№;_/,\'\.$@]|\\[\"\(\)\[\]\{{\}}\:]|\\)+)(?=\s+|\)|$)"
    )

    multi_value_pattern = rf"""\((?P<{ValueType.multi_value}>[:a-zA-Z\"\*0-9=+%#№;\-_\/\\'\,.$&^@!\(\[\]\s|]+)\)"""
    multi_value_check_pattern = r"___field___\s*___operator___\s*\("
    multi_value_delimiter_pattern = r"\s+OR\s+"

    escape_manager = lucene_escape_manager

    wildcard_symbol = "*"

    str_value_manager = lucene_str_value_manager

    @staticmethod
    def create_field_value(field_name: str, operator: Identifier, value: Union[str, list]) -> FieldValue:
        field_name = field_name.replace(".text", "")
        field_name = field_name.replace(".keyword", "")
        return FieldValue(source_name=field_name, operator=operator, value=value)

    @staticmethod
    def clean_multi_value(value: str) -> str:
        return value.strip('"') if value.startswith('"') and value.endswith('"') else value

    def get_operator_and_value(self, match: re.Match, operator: str = OperatorType.EQ) -> tuple[str, StrValue]:  # noqa: PLR0911
        if (num_value := get_match_group(match, group_name=ValueType.number_value)) is not None:
            return operator, StrValue(num_value)

        if (re_value := get_match_group(match, group_name=ValueType.regex_value)) is not None:
            return OperatorType.REGEX, lucene_str_value_manager.from_re_str_to_container(re_value)

        if (n_q_value := get_match_group(match, group_name=ValueType.no_quotes_value)) is not None:
            return operator, lucene_str_value_manager.from_str_to_container(n_q_value)

        if (d_q_value := get_match_group(match, group_name=ValueType.double_quotes_value)) is not None:
            return operator, lucene_str_value_manager.from_str_to_container(d_q_value)

        if (gte_value := get_match_group(match, group_name=ValueType.greater_than_or_equal)) is not None:
            return OperatorType.GTE, StrValue(gte_value)

        if (lte_value := get_match_group(match, group_name=ValueType.less_than_or_equal)) is not None:
            return OperatorType.LTE, StrValue(lte_value)

        return super().get_operator_and_value(match, operator)

    def group_values_by_operator(self, values: list[str], operator: str) -> dict[str, list[StrValue]]:
        mapped_operator = self.map_operator(operator)
        result = {}
        for value in values:
            if value.startswith("/") and value.endswith("/"):
                value = lucene_str_value_manager.from_re_str_to_container(value.strip("/"))
                result.setdefault(OperatorType.REGEX, []).append(value)
            else:
                value = lucene_str_value_manager.from_str_to_container(value)
                operator, value = self.process_value_wildcards(value, mapped_operator)
                result.setdefault(operator, []).append(value)

        return result

    def is_multi_value_flow(self, field_name: str, operator: str, query: str) -> bool:
        check_pattern = self.multi_value_check_pattern
        check_regex = check_pattern.replace("___field___", field_name).replace("___operator___", operator)
        return bool(re.match(check_regex, query))

    def search_keyword(self, query: str) -> tuple[Keyword, str]:
        keyword_search = re.search(self.keyword_pattern, query)
        _, value = self.get_operator_and_value(keyword_search)
        _, value = self.process_value_wildcards(value)
        keyword = Keyword(value=value)
        pos = keyword_search.end()
        return keyword, query[pos:]

    def _check_field_value_match(self, query: str, white_space_pattern: str = r"\s*") -> bool:
        range_value_pattern = f"(?:{self.gte_value_pattern}|{self.lte_value_pattern})"
        range_pattern = rf"{self.field_pattern}{white_space_pattern}:\s*{range_value_pattern}"
        if re.match(range_pattern, query, re.IGNORECASE):
            return True

        return super()._check_field_value_match(query, white_space_pattern=white_space_pattern)

    def tokenize(self, query: str) -> list[Union[FieldValue, Keyword, Identifier]]:
        tokens = super().tokenize(query=query)
        return self.add_and_token_if_missed(tokens=tokens)
