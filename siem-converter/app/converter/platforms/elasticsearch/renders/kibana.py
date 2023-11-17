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

from app.converter.platforms.elasticsearch.const import KIBANA_SEARCH_SOURCE_JSON, KIBANA_RULE, kibana_rule_details
from app.converter.platforms.elasticsearch.mapping import ElasticSearchMappings, elasticsearch_mappings
from app.converter.platforms.elasticsearch.renders.elasticsearch import ElasticSearchQueryRender, ElasticSearchFieldValue
from app.converter.core.mapping import SourceMapping
from app.converter.core.models.platform_details import PlatformDetails
from app.converter.core.operator_types.output import MetaInfoContainer
from app.converter.tools.utils import concatenate_str, get_author_str, get_licence_str, get_mitre_attack_str, \
    get_rule_id_str, get_references_str


class KibanaFieldValue(ElasticSearchFieldValue):
    details: PlatformDetails = kibana_rule_details


class KibanaRuleRender(ElasticSearchQueryRender):
    details: PlatformDetails = kibana_rule_details
    mappings: ElasticSearchMappings = elasticsearch_mappings
    or_token = "OR"
    field_value_map = KibanaFieldValue(or_token=or_token)

    def finalize_query(self, prefix: str, query: str, functions: str, meta_info: MetaInfoContainer,
                       source_mapping: SourceMapping = None, not_supported_functions: list = None):
        query = super().finalize_query(prefix=prefix, query=query, functions=functions, meta_info=meta_info)
        search_source = copy.deepcopy(KIBANA_SEARCH_SOURCE_JSON)
        search_source["query"]["query_string"]["query"] = query
        dumped_rule = json.dumps(search_source, sort_keys=False)
        rule = copy.deepcopy(KIBANA_RULE)
        rule["_source"]["kibanaSavedObjectMeta"]["searchSourceJSON"] = dumped_rule
        rule["_source"]["title"] = meta_info.title
        description = meta_info.description or rule["_source"]["description"]
        description = concatenate_str(description, get_author_str(meta_info.author))
        description = concatenate_str(description, get_rule_id_str(meta_info.id))
        description = concatenate_str(description, get_licence_str(meta_info.license))
        description = concatenate_str(description, get_references_str(meta_info.references))
        rule["_source"]["description"] = concatenate_str(description, get_mitre_attack_str(meta_info.mitre_attack))
        rule_str = json.dumps(rule, indent=4, sort_keys=False)
        if not_supported_functions:
            rendered_not_supported = self.render_not_supported_functions(not_supported_functions)
            return rule_str + rendered_not_supported
        return rule_str
