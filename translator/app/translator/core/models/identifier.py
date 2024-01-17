from app.translator.core.custom_types.tokens import GroupType, LogicalOperatorType, OperatorType


class _IdentifierTokenType(LogicalOperatorType, GroupType, OperatorType):
    pass


class Identifier:
    valid_token_types = _IdentifierTokenType

    def __init__(self, *, token_type: str) -> None:
        if token_type not in self.valid_token_types:
            raise Exception(f"Unexpected token type: {token_type}")

        self.token_type = token_type

    def __repr__(self):
        return f"{self.token_type}"
