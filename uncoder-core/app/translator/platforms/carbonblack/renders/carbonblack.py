from app.translator.const import DEFAULT_VALUE_TYPE
from app.translator.core.custom_types.values import ValueType
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.render import BaseFieldValueRender, PlatformQueryRender
from app.translator.managers import render_manager
from app.translator.platforms.carbonblack.const import carbonblack_query_details
from app.translator.platforms.carbonblack.mapping import CarbonBlackMappings, carbonblack_query_mappings
from app.translator.platforms.carbonblack.str_value_manager import (
    CarbonBlackStrValueManager,
    carbon_black_str_value_manager,
)


class CarbonBlackFieldValueRender(BaseFieldValueRender):
    details: PlatformDetails = carbonblack_query_details
    str_value_manager: CarbonBlackStrValueManager = carbon_black_str_value_manager

    @staticmethod
    def _wrap_str_value(value: str, value_type: str = ValueType.value) -> str:  # noqa: ARG004
        return f'"{value}"'

    @staticmethod
    def _wrap_int_value(value: int) -> str:
        return f'"{value}"'

    def equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.equal_modifier(field=field, value=v) for v in value)})"
        value = self._pre_process_value(field, value, value_type=ValueType.value, wrap_str=True, wrap_int=True)
        return f"{field}:{value}"

    def not_equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            values = [
                self._pre_process_value(field, val, value_type=ValueType.value, wrap_str=True, wrap_int=True)
                for val in value
            ]
            return f"(NOT {field}:({self.or_token.join(values)})"
        value = self._pre_process_value(field, value, value_type=ValueType.value, wrap_str=True, wrap_int=True)
        return f"(NOT {field}:{self.apply_value(value)})"

    def contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            values = self.or_token.join(
                [f"*{self._pre_process_value(field, val, value_type=ValueType.value)}*" for val in value]
            )
            return f"{field}:({values})"
        value = self._pre_process_value(field, value, value_type=ValueType.value)
        return f"{field}:*{value}*"

    def endswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            values = self.or_token.join(
                [f"*{self._pre_process_value(field, val, value_type=ValueType.value)}" for val in value]
            )
            return f"{field}:({values})"
        value = self._pre_process_value(field, value, value_type=ValueType.value)
        return f"{field}:*{value}"

    def startswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            values = self.or_token.join(
                [f"{self._pre_process_value(field, val, value_type=ValueType.value)}*" for val in value]
            )
            return f"{field}:({values}"
        value = self._pre_process_value(field, value, value_type=ValueType.value)
        return f"{field}:{value}*"

    def regex_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.regex_modifier(field=field, value=v) for v in value)})"
        value = self._pre_process_value(field, value, value_type=ValueType.regex_value)
        return f"{field}:/{value}/"

    def keywords(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.keywords(field=field, value=v) for v in value)})"
        value = self._pre_process_value(field, value, value_type=ValueType.value)
        return f"(*{value}*)"

    def is_none(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.is_none(field=field, value=v) for v in value)})"
        return f"NOT _exists_:{field}"

    def is_not_none(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.is_not_none(field=field, value=v) for v in value)})"
        return f"_exists_:{field}"


@render_manager.register
class CarbonBlackQueryRender(PlatformQueryRender):
    details: PlatformDetails = carbonblack_query_details
    mappings: CarbonBlackMappings = carbonblack_query_mappings

    or_token = "OR"
    and_token = "AND"
    not_token = "NOT"

    comment_symbol = "//"

    field_value_render = CarbonBlackFieldValueRender(or_token=or_token)
