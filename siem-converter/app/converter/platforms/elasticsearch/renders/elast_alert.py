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

from app.converter.platforms.elasticsearch.const import ELASTICSEARCH_ALERT, elastalert_details
from app.converter.platforms.elasticsearch.mapping import ElasticSearchMappings, elasticsearch_mappings
from app.converter.platforms.elasticsearch.renders.elasticsearch import ElasticSearchQueryRender, ElasticSearchFieldValue
from app.converter.core.mapping import SourceMapping
from app.converter.core.models.platform_details import PlatformDetails
from app.converter.core.models.parser_output import MetaInfoContainer
from app.converter.tools.utils import get_rule_description_str


SEVERITIES_MAP = {"informational": "5", "low": "4", "medium": "3", "high": "2", "critical": "1"}


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

    def finalize_query(self, prefix: str, query: str, functions: str, meta_info: MetaInfoContainer,
                       source_mapping: SourceMapping = None, not_supported_functions: list = None):
        query = super().finalize_query(prefix=prefix, query=query, functions=functions, meta_info=meta_info)
        rule = ELASTICSEARCH_ALERT.replace("<query_placeholder>", query)
        rule = rule.replace(
            "<description_place_holder>",
            get_rule_description_str(
                description=meta_info.description,
                license=meta_info.license
            )
        )
        rule = rule.replace("<title_place_holder>", meta_info.title)
        rule = rule.replace("<priority_place_holder>", SEVERITIES_MAP[meta_info.severity])
        if not_supported_functions:
            rendered_not_supported = self.render_not_supported_functions(not_supported_functions)
            return rule + rendered_not_supported
        return rule
