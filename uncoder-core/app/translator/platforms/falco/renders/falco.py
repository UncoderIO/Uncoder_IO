"""
Uncoder IO Community Edition License
-----------------------------------------------------------------
Copyright (c) 2024 SOC Prime, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-----------------------------------------------------------------
"""
from typing import ClassVar, Optional

import yaml

from app.translator.const import DEFAULT_VALUE_TYPE
from app.translator.core.custom_types.values import ValueType
from app.translator.core.mapping import LogSourceSignature, SourceMapping
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.models.query_container import MetaInfoContainer
from app.translator.core.models.query_tokens.field import Field
from app.translator.core.render import BaseFieldValueRender, PlatformQueryRender
from app.translator.core.str_value_manager import StrValueManager
from app.translator.managers import render_manager
from app.translator.platforms.falco.const import falco_rule_details
from app.translator.platforms.falco.mapping import FalcoRuleMappings, falco_rule_mappings
from app.translator.platforms.falco.str_value_manager import falco_rule_str_value_manager


class FalcoRuleFieldValueRender(BaseFieldValueRender):
    details = falco_rule_details
    str_value_manager: StrValueManager = falco_rule_str_value_manager

    @staticmethod
    def _wrap_str_value(value: str) -> str:
        return f'"{value}"'

    @staticmethod
    def _wrap_int_value(value: str) -> str:
        return f'"{value}"'

    def equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.equal_modifier(field=field, value=v) for v in value])})"
        return f"{field} = {self._pre_process_value(field, value, wrap_str=True)}"

    def not_equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.not_equal_modifier(field=field, value=v) for v in value])})"
        return f"{field} != {self._pre_process_value(field, value, wrap_str=True)}"

    def less_modifier(self, field: str, value: int) -> str:
        return f"{field} < {self._pre_process_value(field, value)}"

    def less_or_equal_modifier(self, field: str, value: int) -> str:
        return f"{field} <= {self._pre_process_value(field, value)}"

    def greater_modifier(self, field: str, value: int) -> str:
        return f"{field} > {self._pre_process_value(field, value)}"

    def greater_or_equal_modifier(self, field: str, value: int) -> str:
        return f"{field} >= {self._pre_process_value(field, value)}"

    def contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.contains_modifier(field=field, value=v) for v in value])})"
        value = self._pre_process_value(field, value, wrap_str=True, wrap_int=True)
        return f"{field} contains {value}"

    def endswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.endswith_modifier(field=field, value=v) for v in value])})"
        value = self._pre_process_value(field, value, wrap_str=True, wrap_int=True)
        return f"{field} endswith {value}"

    def startswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.startswith_modifier(field=field, value=v) for v in value])})"
        value = self._pre_process_value(field, value, wrap_str=True, wrap_int=True)
        return f"{field} startswith {value}"

    def regex_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.regex_modifier(field=field, value=v) for v in value)})"
        regex_str = self._pre_process_value(field, value, value_type=ValueType.regex_value)
        return f"{field} regex '{regex_str}'"

    def is_none(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.is_none(field=field, value=v) for v in value)})"
        return f"{field} exists"


@render_manager.register
class FalcoRuleRender(PlatformQueryRender):
    details: PlatformDetails = falco_rule_details
    mappings: FalcoRuleMappings = falco_rule_mappings

    or_token = "or"
    and_token = "and"
    not_token = "not"

    comment_symbol = "//"

    field_value_render = FalcoRuleFieldValueRender(or_token=or_token)

    priority_map: ClassVar[dict[str, str]] = {
        "unspecified": "NOTICE",
        "info": "INFORMATIONAL",
        "low": "WARNING",
        "medium": "ERROR",
        "high": "ERROR",
        "critical": "CRITICAL",
    }

    def generate_prefix(self, log_source_signature: Optional[LogSourceSignature], functions_prefix: str = "") -> str:  # noqa: ARG002
        return ""

    def generate_output(self, fields: list[Field], unmapped_fields: list[str], source_mapping: SourceMapping) -> str:
        extra_fields = []
        for field in fields:
            if field.source_name in unmapped_fields:
                extra_fields.append(field.source_name)
            elif generic_field_name := field.get_generic_field_name(source_mapping.source_id):
                extra_field = source_mapping.fields_mapping.get_platform_field_name(generic_field_name)
                if extra_field:
                    extra_fields.append(extra_field)
        extra_fields = [f"{field.replace('.', '_')}=%{field}" for field in extra_fields]
        return f"shell in a container (container_name=%container.name {' '.join(extra_fields)})"

    def finalize_query(
        self,
        prefix: str,
        query: str,
        functions: str,
        meta_info: Optional[MetaInfoContainer] = None,
        source_mapping: Optional[SourceMapping] = None,
        not_supported_functions: Optional[list] = None,
        unmapped_fields: Optional[list[str]] = None,
        *args,  # noqa: ARG002
        **kwargs,  # noqa: ARG002
    ) -> str:
        query = self._join_query_parts(prefix, query, functions)
        rule = {
            "rule": meta_info.title or "Falco Rule",
            "condition": query,
            "desc": meta_info.description or "Falco Rule",
            "output": self.generate_output(meta_info.query_fields, unmapped_fields or [], source_mapping),
            "priority": self.priority_map.get(meta_info.severity or "medium"),
        }
        rule_str = yaml.dump(rule, default_flow_style=False, sort_keys=False)
        rule_str = self.wrap_with_meta_info(rule_str, meta_info)
        rule_str = self.wrap_with_unmapped_fields(rule_str, unmapped_fields)
        return self.wrap_with_not_supported_functions(rule_str, not_supported_functions)
