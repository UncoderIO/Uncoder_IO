"""
Uncoder IO Community Edition License
-----------------------------------------------------------------
Copyright (c) 2023 SOC Prime, Inc.

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

from app.translator.core.custom_types.meta_info import SeverityType
from app.translator.core.mapping import SourceMapping
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.models.query_container import MetaInfoContainer
from app.translator.platforms.elasticsearch.const import ELASTICSEARCH_ALERT, elastalert_details
from app.translator.platforms.elasticsearch.mapping import ElasticSearchMappings, elasticsearch_mappings
from app.translator.platforms.elasticsearch.renders.elasticsearch import (
    ElasticSearchFieldValue,
    ElasticSearchQueryRender,
)
from app.translator.tools.utils import get_rule_description_str

_SEVERITIES_MAP = {SeverityType.low: "4", SeverityType.medium: "3", SeverityType.high: "2", SeverityType.critical: "1"}


class ElasticAlertRuleFieldValue(ElasticSearchFieldValue):
    details: PlatformDetails = elastalert_details


class ElastAlertRuleRender(ElasticSearchQueryRender):
    details: PlatformDetails = elastalert_details
    mappings: ElasticSearchMappings = elasticsearch_mappings

    or_token = "OR"
    and_token = "AND"
    not_token = "NOT"

    field_value_map = ElasticAlertRuleFieldValue(or_token=or_token)
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
        rule = ELASTICSEARCH_ALERT.replace("<query_placeholder>", query)
        rule = rule.replace(
            "<description_place_holder>",
            get_rule_description_str(
                author=meta_info.author,
                description=meta_info.description,
                license_=meta_info.license,
                rule_id=meta_info.id,
            ),
        )
        rule = rule.replace("<title_place_holder>", meta_info.title)
        rule = rule.replace("<priority_place_holder>", _SEVERITIES_MAP[meta_info.severity])
        if not_supported_functions:
            rendered_not_supported = self.render_not_supported_functions(not_supported_functions)
            return rule + rendered_not_supported
        return rule
