from dataclasses import dataclass

from app.translator.core.custom_types.functions import FunctionType
from app.translator.core.models.functions.base import Function
from app.translator.core.models.query_tokens.field import Alias, Field


@dataclass
class RenameArg:
    field_: Field = None
    alias: Alias = None


@dataclass
class RenameFunction(Function):
    name: str = FunctionType.rename
    args: list[RenameArg] = None

    @property
    def fields(self) -> list[Field]:
        fields = []
        for arg in self.args:
            fields.append(arg.field_)

        return fields
