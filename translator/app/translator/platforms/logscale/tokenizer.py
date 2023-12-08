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
from app.translator.core.models.field import Keyword, Field
from app.translator.core.models.identifier import Identifier
from app.translator.core.custom_types.tokens import GroupType, LogicalOperatorType, OperatorType
from app.translator.core.tokenizer import QueryTokenizer
from app.translator.tools.utils import get_match_group


class LogScaleTokenizer(QueryTokenizer, ANDLogicOperatorMixin):
    match_operator_pattern = r"""(?:___field___\s?(?P<match_operator>=|!=))\s?"""
    num_value_pattern = r"(?P<num_value>\d+(?:\.\d+)*)\s*"
    double_quotes_value_pattern = r'"(?P<d_q_value>(?:[:a-zA-Z\*0-9=+%#\-_/,\'\.$&^@!\(\)\{\}\s]|\\\"|\\)*)"\s*'
    re_value_pattern = r"/(?P<re_value>[:a-zA-Z\*0-9=+%#\\\-_\,\"\'\.$&^@!\(\)\{\}\s?]+)/i?\s*"
    _value_pattern = fr"""{num_value_pattern}|{re_value_pattern}|{double_quotes_value_pattern}"""
    keyword_pattern = double_quotes_value_pattern

    wildcard_symbol = "*"

    def get_operator_and_value(self, match: re.Match, operator: str = OperatorType.EQ) -> Tuple[str, Any]:
        if (num_value := get_match_group(match, group_name='num_value')) is not None:
            return operator, num_value

        elif (d_q_value := get_match_group(match, group_name='d_q_value')) is not None:
            return operator, d_q_value

        elif (re_value := get_match_group(match, group_name='re_value')) is not None:
            return OperatorType.REGEX, re_value

        return super().get_operator_and_value(match, operator)

    def __get_identifier(self, query: str) -> (list, str):
        query = query.strip("\n").strip(" ").strip("\n")
        if query.startswith(GroupType.L_PAREN):
            return Identifier(token_type=GroupType.L_PAREN), query[1:]
        elif query.startswith(GroupType.R_PAREN):
            return Identifier(token_type=GroupType.R_PAREN), query[1:]
        elif query.startswith('!'):
            return Identifier(token_type=LogicalOperatorType.NOT), query[1:]
        elif operator_search := re.match(self.operator_pattern, query):
            operator = operator_search.group("operator")
            pos = operator_search.end()
            return Identifier(token_type=operator.lower()), query[pos:]
        elif self.keyword_pattern and re.match(self.keyword_pattern, query):
            return self.search_keyword(query)
        else:
            return self.search_field_value(query)

    def tokenize(self, query: str) -> List[Union[Field, Keyword, Identifier]]:
        tokenized = []
        while query:
            identifier, query = self.__get_identifier(query=query)
            if tokenized:
                if isinstance(identifier, Identifier) and identifier.token_type in (GroupType.L_PAREN, LogicalOperatorType.NOT):
                    if isinstance(tokenized[-1], (Field, Keyword)) or tokenized[-1].token_type == GroupType.R_PAREN:
                        tokenized.append(Identifier(token_type=LogicalOperatorType.AND))
                elif isinstance(identifier, (Field, Keyword)):
                    if isinstance(tokenized[-1], (Field, Keyword)) or tokenized[-1].token_type == GroupType.R_PAREN:
                        tokenized.append(Identifier(token_type=LogicalOperatorType.AND))
            tokenized.append(identifier)
        self._validate_parentheses(tokenized)
        return self.add_and_token_if_missed(tokens=tokenized)
