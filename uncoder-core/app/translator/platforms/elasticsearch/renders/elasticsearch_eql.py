from typing import Optional, Union

from app.translator.const import DEFAULT_VALUE_TYPE
from app.translator.core.const import QUERY_TOKEN_TYPE
from app.translator.core.custom_types.tokens import GroupType
from app.translator.core.custom_types.values import ValueType
from app.translator.core.mapping import LogSourceSignature
from app.translator.core.mixins.tokens import ExtraConditionMixin
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.models.query_tokens.identifier import Identifier
from app.translator.core.render import BaseFieldValueRender, PlatformQueryRender
from app.translator.core.str_value_manager import StrValueManager
from app.translator.managers import render_manager
from app.translator.platforms.base.lucene.mapping import LuceneMappings
from app.translator.platforms.elasticsearch.const import elastic_eql_query_details
from app.translator.platforms.elasticsearch.mapping import elastic_eql_query_mappings
from app.translator.platforms.elasticsearch.str_value_manager import eql_str_value_manager


class ElasticSearchEQLFieldValue(BaseFieldValueRender):
    details: PlatformDetails = elastic_eql_query_details
    str_value_manager: StrValueManager = eql_str_value_manager
    list_token = ", "

    @staticmethod
    def _wrap_str_value(value: str) -> str:
        return f'"{value}"'

    @staticmethod
    def _wrap_int_value(value: int) -> str:
        return f'"{value}"'

    def apply_field(self, field: str) -> str:
        if field.count("-") > 0 or field.count(" ") > 0 or field[0].isdigit():
            return f"`{field}`"
        if field.endswith(".text"):
            return field[:-5]
        return field

    def equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            values = self.list_token.join(
                self._pre_process_value(field, v, value_type=ValueType.value, wrap_str=True, wrap_int=True)
                for v in value
            )
            return f"{self.apply_field(field)} : ({values})"
        value = self._pre_process_value(field, value, value_type=ValueType.value, wrap_str=True, wrap_int=True)
        return f"{self.apply_field(field)} : {value}"

    def less_modifier(self, field: str, value: Union[int, str]) -> str:
        value = self._pre_process_value(field, value, value_type=ValueType.value, wrap_str=True, wrap_int=True)
        return f"{self.apply_field(field)} < {value}"

    def less_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:
        value = self._pre_process_value(field, value, value_type=ValueType.value, wrap_str=True, wrap_int=True)
        return f"{self.apply_field(field)} <= {value}"

    def greater_modifier(self, field: str, value: Union[int, str]) -> str:
        value = self._pre_process_value(field, value, value_type=ValueType.value, wrap_str=True, wrap_int=True)
        return f"{self.apply_field(field)} > {value}"

    def greater_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:
        value = self._pre_process_value(field, value, value_type=ValueType.value, wrap_str=True, wrap_int=True)
        return f"{self.apply_field(field)} >= {value}"

    def not_equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            values = self.list_token.join(
                self._pre_process_value(field, v, value_type=ValueType.value, wrap_str=True, wrap_int=True)
                for v in value
            )
            return f"{self.apply_field(field)} != ({values})"
        value = self._pre_process_value(field, value, value_type=ValueType.value, wrap_str=True, wrap_int=True)
        return f"{self.apply_field(field)} != {value}"

    def contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            values = self.list_token.join(
                f'"*{self._pre_process_value(field, v, value_type=ValueType.value)}*"' for v in value
            )
            return f"{self.apply_field(field)} : ({values})"
        value = self._pre_process_value(field, value, value_type=ValueType.value)
        return f'{self.apply_field(field)} : "*{value}*"'

    def endswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            values = self.list_token.join(
                f'"*{self._pre_process_value(field, v, value_type=ValueType.value)}"' for v in value
            )
            return f"{self.apply_field(field)} : ({values})"
        value = self._pre_process_value(field, value, value_type=ValueType.value)
        return f'{self.apply_field(field)} : "*{value}"'

    def startswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            values = self.list_token.join(
                f'"{self._pre_process_value(field, v, value_type=ValueType.value)}*"' for v in value
            )
            return f"{self.apply_field(field)} : ({values})"
        value = self._pre_process_value(field, value, value_type=ValueType.value)
        return f'{self.apply_field(field)} : "{value}*"'

    def regex_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.regex_modifier(field=field, value=v) for v in value)})"
        value = self._pre_process_value(field, value, value_type=ValueType.regex_value, wrap_int=True)
        return f'{self.apply_field(field)} regex~ "{value}.?"'

    def keywords(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.keywords(field=field, value=v) for v in value)})"
        return self._pre_process_value(field, value, wrap_str=True)

    def is_none(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        return f"{self.apply_field(field)} == null"

    def is_not_none(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        return f"{self.apply_field(field)} != null"


@render_manager.register

class ElasticSearchEQLQueryRender(ExtraConditionMixin, PlatformQueryRender):
    details: PlatformDetails = elastic_eql_query_details
    mappings: LuceneMappings = elastic_eql_query_mappings
    or_token = "or"
    and_token = "and"
    not_token = "not"
    comment_symbol = "//"
    field_value_render = ElasticSearchEQLFieldValue(or_token=or_token)

    def generate_prefix(self, log_source_signature: Optional[LogSourceSignature], functions_prefix: str = "") -> str:  # noqa: ARG002
        return "any where "

    def in_brackets(self, raw_list: list[QUERY_TOKEN_TYPE]) -> list[QUERY_TOKEN_TYPE]:
        return [Identifier(token_type=GroupType.L_PAREN), *raw_list, Identifier(token_type=GroupType.R_PAREN)]
      
