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

import copy
import json

from app.converter.platforms.elasticsearch.const import ELASTICSEARCH_DETECTION_RULE, elasticsearch_rule_details
from app.converter.platforms.elasticsearch.mapping import ElasticSearchMappings, elasticsearch_mappings
from app.converter.platforms.elasticsearch.renders.elasticsearch import ElasticSearchQueryRender, ElasticSearchFieldValue
from app.converter.core.mapping import SourceMapping
from app.converter.core.models.platform_details import PlatformDetails
from app.converter.core.operator_types.output import MetaInfoContainer
from app.converter.tools.utils import concatenate_str, get_mitre_attack_str


class ElasticSearchRuleFieldValue(ElasticSearchFieldValue):
    details: PlatformDetails = elasticsearch_rule_details


class ElasticSearchRuleRender(ElasticSearchQueryRender):
    details: PlatformDetails = elasticsearch_rule_details
    mappings: ElasticSearchMappings = elasticsearch_mappings

    or_token = "OR"
    and_token = "AND"
    not_token = "NOT"

    field_value_map = ElasticSearchRuleFieldValue(or_token=or_token)
    query_pattern = "{prefix} {query} {functions}"

    def finalize_query(self, prefix: str, query: str, functions: str, meta_info: MetaInfoContainer,
                       source_mapping: SourceMapping = None, not_supported_functions: list = None):
        query = super().finalize_query(prefix=prefix, query=query, functions=functions, meta_info=meta_info)
        rule = copy.deepcopy(ELASTICSEARCH_DETECTION_RULE)
        description = meta_info.description or rule["description"]
        mitre_attack_str = get_mitre_attack_str(meta_info.mitre_attack)
        description = concatenate_str(description, mitre_attack_str)

        rule.update({
            "query": query,
            "description": description,
            "name": meta_info.title,
            "rule_id": meta_info.id,
            "author": [meta_info.author],
            "severity": meta_info.severity,
            "references": meta_info.references,
            "license": meta_info.license,
            "tags": meta_info.mitre_attack,
            "false_positives": meta_info.false_positives
        })
        rule_str = json.dumps(rule, indent=4, sort_keys=False)
        if not_supported_functions:
            rendered_not_supported = self.render_not_supported_functions(not_supported_functions)
            return rule_str + rendered_not_supported
        return rule_str
