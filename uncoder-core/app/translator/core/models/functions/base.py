from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional, Union

from app.translator.core.models.query_tokens.field import Alias, Field
from app.translator.core.models.query_tokens.field_field import FieldField
from app.translator.core.models.query_tokens.field_value import FieldValue
from app.translator.core.models.query_tokens.identifier import Identifier
from app.translator.core.models.query_tokens.keyword import Keyword

if TYPE_CHECKING:
    from app.translator.core.models.query_tokens.function_value import FunctionValue


@dataclass
class Function:
    name: str = None
    args: list[
        Union[Alias, Field, FieldField, FieldValue, FunctionValue, Keyword, Function, Identifier, int, str, bool]
    ] = field(default_factory=list)
    alias: Optional[Alias] = None
    raw: str = ""


@dataclass
class ParsedFunctions:
    functions: list[Function] = field(default_factory=list)
    not_supported: list[str] = field(default_factory=list)
    invalid: list[str] = field(default_factory=list)
    aliases: dict[str, Function] = field(default_factory=dict)


@dataclass
class RenderedFunctions:
    rendered_prefix: str = ""
    rendered: str = ""
    not_supported: list[str] = field(default_factory=list)
