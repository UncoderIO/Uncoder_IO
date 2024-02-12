from typing import ClassVar, Union, Optional

from app.translator.core.custom_types.tokens import GroupType, LogicalOperatorType, OperatorType
from app.translator.core.models.field import FieldValue
from app.translator.core.models.identifier import Identifier
from app.translator.core.str_value_processing import StrValue
from app.translator.platforms.sigma.str_value_processing import sigma_str_value_manager

_MULTY_MODIFIER_LEN = 2


class ModifierManager:
    and_token = Identifier(token_type=LogicalOperatorType.AND)
    or_token = Identifier(token_type=LogicalOperatorType.OR)

    modifier_map: ClassVar[dict[str, str]] = {"re": OperatorType.REGEX}

    def __validate_modifiers(self, modifiers: Union[str, list]) -> bool:
        if isinstance(modifiers, list) and len(modifiers) > _MULTY_MODIFIER_LEN:
            raise
        if isinstance(modifiers, list):
            return all(self.__validate_modifiers(modifier) for modifier in modifiers)
        return True

    def map_modifier(self, modifier: str) -> Identifier:
        return Identifier(token_type=self.modifier_map.get(modifier, modifier))

    def modifier_all(self, field_name: str, modifier: str, values: Union[str, list[str]]) -> Union[tuple, list]:
        if (isinstance(values, list) and len(values) == 1) or isinstance(values, str):
            operator = self.map_modifier(modifier=modifier)
            values = self.convert_values_to_str_values(values, modifier)
            return (FieldValue(source_name=field_name, operator=operator, value=values),)

        tokens = []
        for value in values:
            tokens.extend(self.modifier_all(field_name=field_name, modifier=modifier, values=value))
            tokens.append(self.and_token)
        return [Identifier(token_type=GroupType.L_PAREN), *tokens[:-1], Identifier(token_type=GroupType.R_PAREN)]

    @staticmethod
    def __prepare_windash_value(value: str) -> Union[str, list[str]]:
        if value.startswith(r"/"):
            return [value, value.replace(r"/", "-", 1)]
        if value.startswith(r"-"):
            return [value, value.replace("-", r"/", 1)]
        return value

    def modifier_windash(
        self, field_name: str, modifier: Union[str, list], values: Union[str, list[str]]
    ) -> Union[tuple, list]:
        if isinstance(values, list):
            tokens = []
            for value in values:
                tokens.extend(self.modifier_windash(field_name=field_name, modifier=modifier, values=value))
                tokens.append(self.or_token)
            return [Identifier(token_type=GroupType.L_PAREN), *tokens[:-1], Identifier(token_type=GroupType.R_PAREN)]
        operator = self.map_modifier(modifier=modifier)
        values = self.__prepare_windash_value(value=values)
        values = self.convert_values_to_str_values(values, modifier)
        return (FieldValue(source_name=field_name, operator=operator, value=values),)

    def apply_multi_modifier(
        self, field_name: str, modifier: list, values: Union[str, list[str]]
    ) -> Optional[Union[tuple, list]]:
        if modifier[-1] == "all":
            return self.modifier_all(field_name=field_name, modifier=modifier[0], values=values)
        if modifier[-1] == "windash":
            return self.modifier_windash(field_name=field_name, modifier=modifier[0], values=values)

        raise NotImplementedError

    def apply_modifier(self, field_name: str, modifier: list, values: Union[int, str, list[Union[int, str]]]) -> tuple:
        modifier = modifier[0]
        if modifier == "windash":
            modifier = OperatorType.EQ
            return self.modifier_windash(field_name=field_name, modifier=modifier, values=values)
        operator = self.map_modifier(modifier=modifier)
        values = self.convert_values_to_str_values(values, modifier)
        return (FieldValue(source_name=field_name, operator=operator, value=values),)

    @staticmethod
    def convert_values_to_str_values(
            values: Union[int, str, list[Union[int, str]]],
            operator: str
    ) -> Union[StrValue, list[StrValue]]:
        if not isinstance(values, list):
            values = [values]

        if operator == "re":
            return [sigma_str_value_manager.from_re_str_to_container(str(value)) for value in values]
        return [sigma_str_value_manager.from_str_to_container(str(value)) for value in values]

    def create_token(self, field_name: str, modifier: list, value: Union[str, list[str], int]) -> Union[tuple, list]:
        if len(modifier) == _MULTY_MODIFIER_LEN:
            return self.apply_multi_modifier(field_name=field_name, modifier=modifier, values=value)
        return self.apply_modifier(field_name=field_name, modifier=modifier, values=value)

    def generate(self, field_name: str, modifier: list, value: Union[str, list[str], int]) -> Union[tuple, list]:
        if self.__validate_modifiers(modifiers=modifier):
            return self.create_token(field_name=field_name, modifier=modifier, value=value)
