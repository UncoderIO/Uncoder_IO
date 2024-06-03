from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Union

from app.translator.core.models.field import Alias, Field, FieldValue, Keyword
from app.translator.core.models.identifier import Identifier


@dataclass
class Function:
    name: str = None
    args: list[Union[Alias, Field, FieldValue, Keyword, Function, Identifier, str, bool]] = field(default_factory=list)
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
