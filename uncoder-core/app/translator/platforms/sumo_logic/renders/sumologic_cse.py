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
import copy
import json
from typing import Optional
from app.translator.core.mapping import SourceMapping
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.models.query_container import MetaInfoContainer
from app.translator.managers import render_manager
from app.translator.core.render import PlatformQueryRender

from app.translator.platforms.sumo_logic.const import (
    SEVERITY_MAP,
    sumologic_cse_query_details,
    sumologic_cse_rule_details,
    DEFAULT_SUMOLOGIC_CSE_RULE
)
from app.translator.platforms.sumo_logic.mapping import SumoLogicMappings, sumologic_mappings
from app.translator.platforms.sumo_logic.renders.sumologic import SumologicFieldValue



@render_manager.register
class SumologicCSERender(PlatformQueryRender):
    details: PlatformDetails = sumologic_cse_query_details
    mappings: SumoLogicMappings = sumologic_mappings

    or_token = "OR"
    and_token = "AND"
    not_token = "NOT"

    field_value_map = SumologicFieldValue(or_token=or_token)
    query_pattern = "{prefix} {query} {functions}"


@render_manager.register
class SumologicCSERuleRender(PlatformQueryRender):
    details: PlatformDetails = sumologic_cse_rule_details
    mappings: SumoLogicMappings = sumologic_mappings

    or_token = "OR"
    and_token = "AND"
    not_token = "NOT"

    field_value_map = SumologicFieldValue(or_token=or_token)
    query_pattern = "{prefix} {query} {functions}"


    def finalize_query(
        self,
        prefix: str,
        query: str,
        functions: str,
        meta_info: Optional[MetaInfoContainer] = None,
        source_mapping: Optional[SourceMapping] = None,  # noqa: ARG002
        not_supported_functions: Optional[list] = None,
        *args,  # noqa: ARG002
        **kwargs,  # noqa: ARG002
    ) -> str:
        query = super().finalize_query(prefix=prefix, query=query, functions=functions)
        rule = copy.deepcopy(DEFAULT_SUMOLOGIC_CSE_RULE)
        rule["name"] = meta_info.title or rule["name"] if meta_info else rule['name']
        rule["description"] = meta_info.description or rule["description"] if meta_info else rule['description']
        rule["score"] = SEVERITY_MAP.get(meta_info.severity) if meta_info else SEVERITY_MAP['medium']
        rule["expression"] = query
        rule_str = json.dumps(rule, indent=4, sort_keys=False, ensure_ascii=False)
        if not_supported_functions:
            rendered_not_supported = self.render_not_supported_functions(not_supported_functions)
            return rule_str + rendered_not_supported
        return rule_str