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

from app.translator.core.models.field import Field, Keyword
from app.translator.platforms.sigma.models.group import Group
from app.translator.core.models.identifier import Identifier
from app.translator.platforms.sigma.models.operator import Operator, NOT
from app.translator.core.custom_types.tokens import LogicalOperatorType, GroupType


class DataStructureCompiler:
    # pylint: disable=inconsistent-return-statements
    def generate(self, tokens: list, group: Group = None):
        if not tokens:
            group.finalize()
            return group
        group = group if group else Group()
        token = tokens[0]
        if isinstance(token, (Field, Keyword)):
            group += token
            return self.generate(tokens=tokens[1::], group=group)
        elif token.token_type == LogicalOperatorType.OR or token.token_type == LogicalOperatorType.AND:
            group.items = Operator(operator_type=token.token_type)
            return self.generate(tokens=tokens[1::], group=group)
        elif token.token_type == LogicalOperatorType.NOT:
            if isinstance(tokens[1], (Field, Keyword)):
                tokens.insert(2, Identifier(token_type=GroupType.R_PAREN))
                tokens.insert(1, Identifier(token_type=GroupType.L_PAREN))
            sub_group = Group()
            sub_group.items = NOT()
            not_sub_group, new_tokens = self.generate(tokens=tokens[1::], group=sub_group)
            group += not_sub_group
            return self.generate(new_tokens, group)
        elif token.token_type == GroupType.L_PAREN:
            sub_group, new_tokens = self.generate(tokens=tokens[1::])
            if not sub_group.is_null:
                group += sub_group
            if isinstance(group.items, NOT):
                group.finalize()
                return group, new_tokens
            return self.generate(new_tokens, group)
        elif token.token_type == GroupType.R_PAREN:
            group.finalize()
            return group, tokens[1::]
