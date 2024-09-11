from typing import Union

from app.translator.core.custom_types.tokens import STR_SEARCH_OPERATORS
from app.translator.core.models.functions.base import Function
<<<<<<< HEAD
=======
from app.translator.core.models.query_tokens.field import BaseFieldsGetter, Field
>>>>>>> main
from app.translator.core.models.query_tokens.identifier import Identifier
from app.translator.core.models.query_tokens.value import Value
from app.translator.core.str_value_manager import StrValue


<<<<<<< HEAD
class FunctionValue(Value):
=======
class FunctionValue(BaseFieldsGetter, Value):
>>>>>>> main
    def __init__(self, function: Function, operator: Identifier, value: Union[int, str, StrValue, list, tuple]):
        super().__init__(value, cast_to_int=operator.token_type not in STR_SEARCH_OPERATORS)
        self.function = function
        self.operator = operator
<<<<<<< HEAD
=======

    @property
    def fields(self) -> list[Field]:
        return self.function.fields
>>>>>>> main
