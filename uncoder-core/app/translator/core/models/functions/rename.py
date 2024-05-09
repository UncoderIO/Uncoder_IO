from dataclasses import dataclass

from app.translator.core.custom_types.functions import FunctionType
from app.translator.core.models.field import Field
from app.translator.core.models.functions.base import Function


@dataclass
class RenameArg:
    field_: Field = None
    alias: str = None


@dataclass
class RenameFunction(Function):
    name: str = FunctionType.rename
    args: list[RenameArg] = None
