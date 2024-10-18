from typing import Union

from app.translator.const import DEFAULT_VALUE_TYPE
from app.translator.core.custom_types.values import ValueType
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.render import BaseFieldValueRender, PlatformQueryRender
from app.translator.core.str_value_manager import StrValueManager
from app.translator.managers import render_manager
from app.translator.platforms.sentinel_one.const import sentinel_one_power_query_details
from app.translator.platforms.sentinel_one.mapping import (
    SentinelOnePowerQueryMappings,
    sentinel_one_power_query_query_mappings,
)
from app.translator.platforms.sentinel_one.str_value_manager import sentinel_one_power_query_str_value_manager


class SentinelOnePowerQueryFieldValue(BaseFieldValueRender):
    details: PlatformDetails = sentinel_one_power_query_details
    str_value_manager: StrValueManager = sentinel_one_power_query_str_value_manager
    list_token = ", "

    @staticmethod
    def _wrap_str_value(value: str) -> str:
        return f'"{value}"'

    def equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            values = self.list_token.join(
                self._pre_process_value(field, v, value_type=ValueType.value, wrap_str=True) for v in value
            )
            return f"{field} in ({values})"
        value = self._pre_process_value(field, value, value_type=ValueType.value, wrap_str=True)
        return f"{field} = {value}"

    def less_modifier(self, field: str, value: Union[int, str]) -> str:
        value = self._pre_process_value(field, value, value_type=ValueType.value, wrap_str=True)
        return f"{field} < {value}"

    def less_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:
        value = self._pre_process_value(field, value, value_type=ValueType.value, wrap_str=True)
        return f"{field} <= {value}"

    def greater_modifier(self, field: str, value: Union[int, str]) -> str:
        value = self._pre_process_value(field, value, value_type=ValueType.value, wrap_str=True)
        return f"{field} > {value}"

    def greater_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:
        value = self._pre_process_value(field, value, value_type=ValueType.value, wrap_str=True)
        return f"{field} >= {value}"

    def not_equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            values = self.list_token.join(
                self._pre_process_value(field, v, value_type=ValueType.value, wrap_str=True, wrap_int=True)
                for v in value
            )
            return f"{field} != ({values})"
        value = self._pre_process_value(field, value, value_type=ValueType.value, wrap_str=True, wrap_int=True)
        return f"{field} != {value}"

    def contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            values = self.list_token.join(
                self._pre_process_value(field, v, value_type=ValueType.value, wrap_str=True, wrap_int=True)
                for v in value
            )
            return f"{field} contains ({values})"
        value = self._pre_process_value(field, value, value_type=ValueType.value)
        return f"{field} contains {value}"

    def endswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        return self.contains_modifier(field, value)

    def startswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        return self.contains_modifier(field, value)

    def regex_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            values = self.list_token.join(
                self._pre_process_value(field, v, value_type=ValueType.regex_value, wrap_str=True, wrap_int=True)
                for v in value
            )
            return f"{field} matches ({values})"
        value = self._pre_process_value(field, value, value_type=ValueType.regex_value, wrap_str=True, wrap_int=True)
        return f"{field} matches {value}"

    def is_none(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        return f'not ({field} matches "\\.*")'

    def is_not_none(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        return f'{field} matches "\\.*"'


@render_manager.register
class SentinelOnePowerQueryRender(PlatformQueryRender):
    details: PlatformDetails = sentinel_one_power_query_details
    mappings: SentinelOnePowerQueryMappings = sentinel_one_power_query_query_mappings
    or_token = "or"
    and_token = "and"
    not_token = "not"
    comment_symbol = "//"
    field_value_render = SentinelOnePowerQueryFieldValue(or_token=or_token)
