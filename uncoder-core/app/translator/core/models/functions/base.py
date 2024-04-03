from __future__ import annotations

from dataclasses import dataclass, field
from typing import Union

from app.translator.core.models.field import Field, FieldValue, Keyword
from app.translator.core.models.identifier import Identifier


@dataclass
class Function:
    name: str = None
    args: list[Union[Field, FieldValue, Keyword, Function, Identifier]] = field(default_factory=list)
    as_clause: str = None
    by_clauses: list[Field] = field(default_factory=list)
    raw: str = ""


@dataclass
class ParsedFunctions:
    functions: list[Function] = field(default_factory=list)
    not_supported: list[str] = field(default_factory=list)
    invalid: list[str] = field(default_factory=list)


@dataclass
class RenderedFunctions:
    rendered: str = ""
    not_supported: list[str] = field(default_factory=list)
