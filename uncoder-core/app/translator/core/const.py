from typing import Union

from app.translator.core.models.field import Alias, Field, FieldValue, Keyword
from app.translator.core.models.function_value import FunctionValue
from app.translator.core.models.identifier import Identifier

QUERY_TOKEN_TYPE = Union[FieldValue, FunctionValue, Keyword, Identifier, Field, Alias]
