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
from typing import Optional

import ujson

from app.translator.core.mapping import SourceMapping
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.models.query_container import MetaInfoContainer
from app.translator.platforms.elasticsearch.const import KIBANA_RULE, KIBANA_SEARCH_SOURCE_JSON, kibana_rule_details
from app.translator.platforms.elasticsearch.mapping import ElasticSearchMappings, elasticsearch_mappings
from app.translator.platforms.elasticsearch.renders.elasticsearch import (
    ElasticSearchFieldValue,
    ElasticSearchQueryRender,
)
from app.translator.tools.utils import get_rule_description_str


class KibanaFieldValue(ElasticSearchFieldValue):
    details: PlatformDetails = kibana_rule_details


class KibanaRuleRender(ElasticSearchQueryRender):
    details: PlatformDetails = kibana_rule_details
    mappings: ElasticSearchMappings = elasticsearch_mappings
    or_token = "OR"
    field_value_map = KibanaFieldValue(or_token=or_token)

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
        search_source = copy.deepcopy(KIBANA_SEARCH_SOURCE_JSON)
        search_source["query"]["query_string"]["query"] = query
        dumped_rule = ujson.dumps(search_source, sort_keys=False, escape_forward_slashes=False)
        rule = copy.deepcopy(KIBANA_RULE)
        rule["_source"]["kibanaSavedObjectMeta"]["searchSourceJSON"] = dumped_rule
        rule["_source"]["title"] = meta_info.title
        rule["_source"]["description"] = get_rule_description_str(
            description=meta_info.description or rule["_source"]["description"],
            author=meta_info.author,
            rule_id=meta_info.id,
            license_=meta_info.license,
            references=meta_info.references,
        )
        rule_str = ujson.dumps(rule, indent=4, sort_keys=False)
        if not_supported_functions:
            rendered_not_supported = self.render_not_supported_functions(not_supported_functions)
            return rule_str + rendered_not_supported
        return rule_str
