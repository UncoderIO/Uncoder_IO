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
from typing import Optional

import yaml

from app.translator.const import DEFAULT_VALUE_TYPE
from app.translator.core.mapping import LogSourceSignature, SourceMapping
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.models.query_container import MetaInfoContainer
from app.translator.core.render import BaseFieldValueRender, PlatformQueryRender
from app.translator.core.str_value_manager import StrValueManager
from app.translator.managers import render_manager
from app.translator.platforms.falco.const import falco_rule_details
from app.translator.platforms.falco.mapping import falco_rule_mappings, FalcoRuleMappings


class FalcoFieldValueRender(BaseFieldValueRender):
    details = falco_rule_details
    str_value_manager: StrValueManager = None
    #
    # def equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
    #     raise UnsupportedRenderMethod(platform_name=self.details.name, method=OperatorType.EQ.capitalize())

    # def not_equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
    #     raise UnsupportedRenderMethod(platform_name=self.details.name, method=OperatorType.NOT_EQ.capitalize())
    #
    # def less_modifier(self, field: str, value: Union[int, str]) -> str:  # noqa: ARG002
    #     raise UnsupportedRenderMethod(platform_name=self.details.name, method=OperatorType.LT.capitalize())
    #
    # def less_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:  # noqa: ARG002
    #     raise UnsupportedRenderMethod(platform_name=self.details.name, method=OperatorType.LTE.capitalize())
    #
    # def greater_modifier(self, field: str, value: Union[int, str]) -> str:  # noqa: ARG002
    #     raise UnsupportedRenderMethod(platform_name=self.details.name, method=OperatorType.GT.capitalize())
    #
    # def greater_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:  # noqa: ARG002
    #     raise UnsupportedRenderMethod(platform_name=self.details.name, method=OperatorType.GTE.capitalize())
    #
    # def contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
    #     raise UnsupportedRenderMethod(platform_name=self.details.name, method=OperatorType.CONTAINS.capitalize())
    #
    # def not_contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
    #     raise UnsupportedRenderMethod(platform_name=self.details.name, method=OperatorType.NOT_CONTAINS.capitalize())
    #
    # def endswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
    #     raise UnsupportedRenderMethod(platform_name=self.details.name, method=OperatorType.ENDSWITH.capitalize())
    #
    # def not_endswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
    #     raise UnsupportedRenderMethod(platform_name=self.details.name, method=OperatorType.NOT_ENDSWITH.capitalize())
    #
    # def startswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
    #     raise UnsupportedRenderMethod(platform_name=self.details.name, method=OperatorType.STARTSWITH.capitalize())
    #
    # def not_startswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
    #     raise UnsupportedRenderMethod(platform_name=self.details.name, method=OperatorType.NOT_STARTSWITH.capitalize())
    #
    # def regex_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
    #     raise UnsupportedRenderMethod(platform_name=self.details.name, method=OperatorType.REGEX.capitalize())
    #
    # def not_regex_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
    #     raise UnsupportedRenderMethod(platform_name=self.details.name, method=OperatorType.NOT_REGEX.capitalize())
    #
    # def keywords(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
    #     raise UnsupportedRenderMethod(platform_name=self.details.name, method=OperatorType.KEYWORD.capitalize())
    #
    # def is_none(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
    #     raise UnsupportedRenderMethod(platform_name=self.details.name, method=OperatorType.IS_NONE.capitalize())
    #
    # def is_not_none(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
    #     raise UnsupportedRenderMethod(platform_name=self.details.name, method=OperatorType.IS_NOT_NONE.capitalize())


@render_manager.register
class FalcoRuleRender(PlatformQueryRender):
    details: PlatformDetails = falco_rule_details
    mappings: FalcoRuleMappings = falco_rule_mappings

    or_token = "or"
    and_token = "and"
    not_token = "not"

    comment_symbol = "//"

    field_value_render = FalcoFieldValueRender(or_token=or_token)

    def generate_prefix(self, log_source_signature: Optional[LogSourceSignature], functions_prefix: str = "") -> str:  # noqa: ARG002
        return ""


    def finalize_query(
        self,
        prefix: str,
        query: str,
        functions: str,
        meta_info: Optional[MetaInfoContainer] = None,
        source_mapping: Optional[SourceMapping] = None,  # noqa: ARG002
        not_supported_functions: Optional[list] = None,
        unmapped_fields: Optional[list[str]] = None,
        *args,  # noqa: ARG002
        **kwargs,  # noqa: ARG002
    ) -> str:
        query = super().finalize_query(prefix=prefix, query=query, functions=functions)
        default_output = "shell in a container (user=%user.name container_id=%container.id container_name=%container.name)"
        rule = {
            "rule": meta_info.title or "Falco Rule",
            "condition": query,
            "desc": meta_info.description or "Falco Rule",
            "output": default_output,
            "priority": "alert",
        }
        rule = yaml.dump(rule, default_flow_style=False, sort_keys=False)
        return rule