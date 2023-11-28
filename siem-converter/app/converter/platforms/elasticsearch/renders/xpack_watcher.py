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

from app.converter.platforms.elasticsearch.mapping import ElasticSearchMappings, elasticsearch_mappings
from app.converter.platforms.elasticsearch.renders.elasticsearch import ElasticSearchQueryRender, ElasticSearchFieldValue
from app.converter.platforms.elasticsearch.const import XPACK_WATCHER_RULE, xpack_watcher_details
from app.converter.core.mapping import SourceMapping
from app.converter.core.models.platform_details import PlatformDetails
from app.converter.core.models.parser_output import MetaInfoContainer
from app.converter.tools.utils import concatenate_str, get_author_str, get_licence_str, get_mitre_attack_str


class XpackWatcherRuleFieldValue(ElasticSearchFieldValue):
    details: PlatformDetails = xpack_watcher_details


class XPackWatcherRuleRender(ElasticSearchQueryRender):
    details: PlatformDetails = xpack_watcher_details
    mappings: ElasticSearchMappings = elasticsearch_mappings
    or_token = "OR"
    field_value_map = XpackWatcherRuleFieldValue(or_token=or_token)

    def finalize_query(self, prefix: str, query: str, functions: str, meta_info: MetaInfoContainer,
                       source_mapping: SourceMapping = None, not_supported_functions: list = None):
        query = super().finalize_query(prefix=prefix, query=query, functions=functions, meta_info=meta_info)
        rule = copy.deepcopy(XPACK_WATCHER_RULE)
        description = concatenate_str(meta_info.description, get_author_str(meta_info.author))
        description = concatenate_str(description, get_licence_str(meta_info.license))
        description = concatenate_str(description, get_mitre_attack_str(meta_info.mitre_attack))
        rule["metadata"].update({
            "query": query,
            "title": meta_info.title,
            "description": description,
            "tags": meta_info.mitre_attack
        })
        rule["input"]["search"]["request"]["body"]["query"]["bool"]["must"][0]["query_string"]["query"] = query
        indices = source_mapping and [str(source_mapping.log_source_signature)] or []
        rule["input"]["search"]["request"]["indices"] = indices
        rule["actions"]["send_email"]["email"]["subject"] = meta_info.title
        rule_str = json.dumps(rule, indent=4, sort_keys=False)
        if not_supported_functions:
            rendered_not_supported = self.render_not_supported_functions(not_supported_functions)
            return rule_str + rendered_not_supported
        return rule_str
