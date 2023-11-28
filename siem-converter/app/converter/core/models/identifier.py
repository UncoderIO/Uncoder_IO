from dataclasses import dataclass

from app.converter.core.custom_types.tokens import LogicalOperatorType, OperatorType, GroupType


class _IdentifierTokenType(LogicalOperatorType, OperatorType, GroupType):
    pass


@dataclass
class Identifier:
    def __init__(self, *, token_type: str) -> None:
        if token_type not in _IdentifierTokenType:
            raise Exception(f"Unexpected token type: {token_type}")

        self.token_type = token_type

    def __repr__(self):
        return f"{self.token_type}"
