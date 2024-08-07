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

from app.translator.core.custom_types.meta_info import SeverityType
from app.translator.core.mapping import SourceMapping
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.models.query_container import MetaInfoContainer
from app.translator.managers import render_manager
from app.translator.platforms.base.lucene.mapping import LuceneMappings
from app.translator.platforms.elasticsearch.const import ELASTICSEARCH_ALERT, elastalert_details
from app.translator.platforms.elasticsearch.mapping import elastalert_mappings
from app.translator.platforms.elasticsearch.renders.elasticsearch import (
    ElasticSearchFieldValue,
    ElasticSearchQueryRender,
)
from app.translator.tools.utils import get_rule_description_str

_AUTOGENERATED_TEMPLATE = "Autogenerated ElastAlert"
_SEVERITIES_MAP = {SeverityType.low: "4", SeverityType.medium: "3", SeverityType.high: "2", SeverityType.critical: "1"}


class ElasticAlertRuleFieldValue(ElasticSearchFieldValue):
    details: PlatformDetails = elastalert_details


@render_manager.register
class ElastAlertRuleRender(ElasticSearchQueryRender):
    details: PlatformDetails = elastalert_details
    mappings: LuceneMappings = elastalert_mappings

    or_token = "OR"
    and_token = "AND"
    not_token = "NOT"

    field_value_render = ElasticAlertRuleFieldValue(or_token=or_token)

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
        rule = ELASTICSEARCH_ALERT.replace("<query_placeholder>", query)
        mitre_attack = []
        if meta_info and meta_info.mitre_attack:
            mitre_attack.extend([technique.technique_id for technique in meta_info.mitre_attack.techniques])
            mitre_attack.extend([tactic.name for tactic in meta_info.mitre_attack.tactics])
        rule = rule.replace(
            "<description_place_holder>",
            get_rule_description_str(
                author=meta_info.author,
                description=meta_info.description or _AUTOGENERATED_TEMPLATE,
                license_=meta_info.license,
                rule_id=meta_info.id,
                mitre_attack=mitre_attack,
            ),
        )
        rule = rule.replace("<title_place_holder>", meta_info.title or _AUTOGENERATED_TEMPLATE)
        rule = rule.replace("<priority_place_holder>", _SEVERITIES_MAP[meta_info.severity])
        rule = self.wrap_with_unmapped_fields(rule, unmapped_fields)
        return self.wrap_with_not_supported_functions(rule, not_supported_functions)
