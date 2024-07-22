from app.translator.core.const import QUERY_TOKEN_TYPE
from app.translator.core.custom_types.tokens import GroupType, LogicalOperatorType
from app.translator.core.models.query_tokens.field_field import FieldField
from app.translator.core.models.query_tokens.field_value import FieldValue
from app.translator.core.models.query_tokens.function_value import FunctionValue
from app.translator.core.models.query_tokens.identifier import Identifier
from app.translator.core.models.query_tokens.keyword import Keyword


class ANDLogicOperatorMixin:
    @staticmethod
    def get_missed_and_token_indices(tokens: list[QUERY_TOKEN_TYPE]) -> list[int]:
        missed_and_indices = []
        for index in range(len(tokens) - 1):
            token = tokens[index]
            next_token = tokens[index + 1]
            if (
                isinstance(token, (FieldField, FieldValue, FunctionValue, Keyword))
                or isinstance(token, Identifier)
                and token.token_type == GroupType.R_PAREN
            ) and not (
                isinstance(next_token, Identifier)
                and (next_token.token_type in (LogicalOperatorType.AND, LogicalOperatorType.OR, GroupType.R_PAREN))
            ):
                missed_and_indices.append(index + 1)
        return list(reversed(missed_and_indices))

    def add_and_token_if_missed(self, tokens: list[QUERY_TOKEN_TYPE]) -> list[QUERY_TOKEN_TYPE]:
        indices = self.get_missed_and_token_indices(tokens=tokens)
        for index in indices:
            tokens.insert(index, Identifier(token_type=LogicalOperatorType.AND))
        return tokens
