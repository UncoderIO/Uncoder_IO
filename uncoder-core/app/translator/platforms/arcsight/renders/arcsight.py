from typing import Optional, Union

from app.translator.const import DEFAULT_VALUE_TYPE
from app.translator.core.custom_types.values import ValueType
from app.translator.core.mapping import LogSourceSignature
from app.translator.core.mixins.tokens import ExtraConditionMixin
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.render import BaseFieldValueRender, PlatformQueryRender
from app.translator.core.str_value_manager import StrValue, StrValueManager
from app.translator.managers import render_manager
from app.translator.platforms.arcsight.const import arcsight_query_details
from app.translator.platforms.arcsight.mapping import ArcSightMappings, arcsight_query_mappings
from app.translator.platforms.arcsight.str_value_manager import arcsight_str_value_manager


class ArcSightFieldValue(BaseFieldValueRender):
    details: PlatformDetails = arcsight_query_details
    str_value_manager: StrValueManager = arcsight_str_value_manager

    @staticmethod
    def _wrap_str_value(value: str) -> str:
        return f'"{value}"'

    @staticmethod
    def _wrap_int_value(value: int) -> str:
        return f'"{value}"'

    def equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.equal_modifier(field, val) for val in value)})"
        value = self._pre_process_value(field, value, value_type=ValueType.value, wrap_str=True)
        return f"{field} = {value}"

    def less_modifier(self, field: str, value: Union[int, str, StrValue]) -> str:
        return f"{field} < {self._pre_process_value(field, value, wrap_str=True)}"

    def less_or_equal_modifier(self, field: str, value: Union[int, str, StrValue]) -> str:
        return f"{field} <= {self._pre_process_value(field, value, wrap_str=True)}"

    def greater_modifier(self, field: str, value: Union[int, str, StrValue]) -> str:
        return f"{field} > {self._pre_process_value(field, value, wrap_str=True)}"

    def greater_or_equal_modifier(self, field: str, value: Union[int, str, StrValue]) -> str:
        return f"{field} > {self._pre_process_value(field, value, wrap_str=True)}"

    def not_equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.not_equal_modifier(field, val) for val in value)})"
        value = self._pre_process_value(field, value, value_type=ValueType.value, wrap_str=True)
        return f"{field} != {value}"

    def is_none(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.is_none(field=field, value=v) for v in value)})"
        return f"NOT _exists_:{field}"

    def is_not_none(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.is_not_none(field=field, value=v) for v in value)})"
        return f"_exists_:{field}"

    def contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.contains_modifier(field, val) for val in value)})"
        value = self._wrap_str_value(value)
        return f"{field} CONTAINS {value}"

    def endswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.endswith_modifier(field, val) for val in value)})"
        value = self._wrap_str_value(value)
        return f"{field} ENDSWITH {value}"

    def startswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.startswith_modifier(field, val) for val in value)})"
        value = self._wrap_str_value(value)
        return f"{field} STARTSWITH {value}"

    def regex_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.regex_modifier(field, val) for val in value)})"
        value = self._wrap_str_value(value)
        return f"{field} CONTAINS {value}"


@render_manager.register
class ArcSightQueryRender(ExtraConditionMixin, PlatformQueryRender):
    details: PlatformDetails = arcsight_query_details
    mappings: ArcSightMappings = arcsight_query_mappings

    or_token = "OR"
    and_token = "AND"
    not_token = "NOT"

    comment_symbol = "//"

    field_value_render = ArcSightFieldValue(or_token=or_token)

    def generate_prefix(self, log_source_signature: Optional[LogSourceSignature], functions_prefix: str = "") -> str:  # noqa: ARG002
        return ""
