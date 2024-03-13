from typing import Union

from app.translator.core.custom_types.tokens import GroupType, LogicalOperatorType
from app.translator.core.models.field import FieldValue, Keyword
from app.translator.core.models.identifier import Identifier


class ANDLogicOperatorMixin:
    @staticmethod
    def get_missed_and_token_indices(tokens: list[Union[FieldValue, Keyword, Identifier]]) -> list[int]:
        missed_and_indices = []
        for index in range(len(tokens) - 1):
            token = tokens[index]
            next_token = tokens[index + 1]
            if (
                isinstance(token, (FieldValue, Keyword))
                or isinstance(token, Identifier)
                and token.token_type == GroupType.R_PAREN
            ) and not (
                isinstance(next_token, Identifier)
                and (next_token.token_type in (LogicalOperatorType.AND, LogicalOperatorType.OR, GroupType.R_PAREN))
            ):
                missed_and_indices.append(index + 1)
        return list(reversed(missed_and_indices))

    def add_and_token_if_missed(
        self, tokens: list[Union[FieldValue, Keyword, Identifier]]
    ) -> list[Union[FieldValue, Keyword, Identifier]]:
        indices = self.get_missed_and_token_indices(tokens=tokens)
        for index in indices:
            tokens.insert(index, Identifier(token_type=LogicalOperatorType.AND))
        return tokens
