from typing import Union

from app.translator.core.models.query_tokens.field import Alias, Field
from app.translator.core.models.query_tokens.field_field import FieldField
from app.translator.core.models.query_tokens.field_value import FieldValue
from app.translator.core.models.query_tokens.function_value import FunctionValue
from app.translator.core.models.query_tokens.identifier import Identifier
from app.translator.core.models.query_tokens.keyword import Keyword

QUERY_TOKEN_TYPE = Union[FieldField, FieldValue, FunctionValue, Keyword, Identifier, Field, Alias]
