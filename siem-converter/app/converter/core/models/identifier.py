from dataclasses import dataclass

from app.converter.core.operator_types.tokens import ValidTokens


@dataclass
class Identifier:
    def __init__(self, *, token_type: str) -> None:
        if token_type not in ValidTokens:
            raise Exception(f"Unexpected token type: {token_type}")

        self.token_type = token_type

    def __repr__(self):
        return f"{self.token_type}"
