from typing import Union

from app.translator.core.models.field import Alias, Field, FieldValue, Keyword
from app.translator.core.models.identifier import Identifier

TOKEN_TYPE = Union[FieldValue, Keyword, Identifier, Field, Alias]
