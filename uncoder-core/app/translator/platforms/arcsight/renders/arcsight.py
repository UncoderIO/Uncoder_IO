from typing import Optional, Union

from app.translator.const import DEFAULT_VALUE_TYPE
from app.translator.core.custom_types.tokens import GroupType, OperatorType, LogicalOperatorType
from app.translator.core.custom_types.values import ValueType
from app.translator.core.mapping import LogSourceSignature, SourceMapping
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.models.query_container import TokenizedQueryContainer
from app.translator.core.models.query_tokens.field_value import FieldValue
from app.translator.core.models.query_tokens.identifier import Identifier
from app.translator.core.render import BaseFieldValueRender, PlatformQueryRender
from app.translator.core.str_value_manager import StrValueManager, StrValue
from app.translator.managers import render_manager
from app.translator.platforms.arcsight.const import arcsight_query_details
from app.translator.platforms.arcsight.mapping import arcsight_query_mappings, ArcSightMappings
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
        value = self._pre_process_value(field, value, value_type=ValueType.value, wrap_str=True, wrap_int=True)
        return f"{field} = {value}"

    def less_modifier(self, field: str, value: Union[int, str, StrValue]) -> str:
        return f"{field} < {self._pre_process_value(field, value)}"

    def less_or_equal_modifier(self, field: str, value: Union[int, str, StrValue]) -> str:
        return f"{field} <= {self._pre_process_value(field, value)}"

    def greater_modifier(self, field: str, value: Union[int, str, StrValue]) -> str:
        return f"{field} > {self._pre_process_value(field, value)}"

    def greater_or_equal_modifier(self, field: str, value: Union[int, str, StrValue]) -> str:
        return f"{field} > {self._pre_process_value(field, value)}"

    def not_equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.not_equal_modifier(field, val) for val in value)})"
        value = self._pre_process_value(field, value, value_type=ValueType.value, wrap_str=True, wrap_int=True)
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
        value = self._pre_process_value(field, value, value_type=ValueType.value, wrap_str=True, wrap_int=True)
        return f"{field} CONTAINS {value}"

    def endswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.endswith_modifier(field, val) for val in value)})"
        value = self._pre_process_value(field, value, value_type=ValueType.value, wrap_str=True, wrap_int=True)
        return f"{field} ENDSWITH {value}"

    def startswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.startswith_modifier(field, val) for val in value)})"
        value = self._pre_process_value(field, value, value_type=ValueType.value, wrap_str=True, wrap_int=True)
        return f"{field} STARTSWITH {value}"

    # def regex_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:


@render_manager.register
class ArcSightQueryRender(PlatformQueryRender):
    details: PlatformDetails = arcsight_query_details
    mappings: ArcSightMappings = arcsight_query_mappings

    or_token = "OR"
    and_token = "AND"
    not_token = "NOT"

    comment_symbol = "//"

    field_value_render = ArcSightFieldValue(or_token=or_token)

    def generate_prefix(self, log_source_signature: Optional[LogSourceSignature], functions_prefix: str = "") -> str:  # noqa: ARG002
        return ""

    def in_brackets(self, raw_list: list) -> list:
        l_paren = Identifier(token_type=GroupType.L_PAREN)
        r_paren = Identifier(token_type=GroupType.R_PAREN)
        return [l_paren, *raw_list, r_paren]

    def _generate_from_tokenized_query_container_by_source_mapping(
        self, query_container: TokenizedQueryContainer, source_mapping: SourceMapping
    ) -> str:
        unmapped_fields = self.mappings.check_fields_mapping_existence(
            query_container.meta_info.query_fields,
            query_container.meta_info.function_fields_map,
            self.platform_functions.manager.supported_render_names,
            source_mapping,
        )
        rendered_functions = self.generate_functions(query_container.functions.functions, source_mapping)
        prefix = self.generate_prefix(source_mapping.log_source_signature, rendered_functions.rendered_prefix)

        if source_mapping.raw_log_fields:
            defined_raw_log_fields = self.generate_raw_log_fields(
                fields=query_container.meta_info.query_fields + query_container.meta_info.function_fields,
                source_mapping=source_mapping,
            )
            prefix += f"\n{defined_raw_log_fields}"
        if source_mapping.conditions:
            extra_tokens = []
            for field, value in source_mapping.conditions.items():
                extra_tokens.extend([
                    FieldValue(source_name=field, operator=Identifier(token_type=OperatorType.EQ), value=value),
                    Identifier(token_type=LogicalOperatorType.AND)
                ])
            query_container.tokens = [*extra_tokens, *query_container.tokens]
        query = self.generate_query(tokens=query_container.tokens, source_mapping=source_mapping)
        not_supported_functions = query_container.functions.not_supported + rendered_functions.not_supported
        return self.finalize_query(
            prefix=prefix,
            query=query,
            functions=rendered_functions.rendered,
            not_supported_functions=not_supported_functions,
            unmapped_fields=unmapped_fields,
            meta_info=query_container.meta_info,
            source_mapping=source_mapping,
        )
