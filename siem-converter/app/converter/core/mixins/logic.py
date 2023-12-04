from typing import List, Union

from app.converter.core.models.field import Field, Keyword
from app.converter.core.models.identifier import Identifier
from app.converter.core.custom_types.tokens import LogicalOperatorType, GroupType


class ANDLogicOperatorMixin:

    @staticmethod
    def get_missed_and_token_indices(tokens: List[Union[Field, Keyword, Identifier]]) -> List[int]:
        missed_and_indices = []
        for index in range(len(tokens) - 1):
            token = tokens[index]
            next_token = tokens[index + 1]
            if (isinstance(token, (Field, Keyword))
                    and not (isinstance(next_token, Identifier) and (
                                    next_token.token_type in LogicalOperatorType
                                    or next_token.token_type == GroupType.R_PAREN))):
                missed_and_indices.append(index + 1)
        return reversed(missed_and_indices)

    def add_and_token_if_missed(self, tokens: List[Union[Field, Keyword, Identifier]]) -> List[Union[Field, Keyword, Identifier]]:
        indices = self.get_missed_and_token_indices(tokens=tokens)
        for index in indices:
            tokens.insert(index, Identifier(token_type=LogicalOperatorType.AND))
        return tokens
