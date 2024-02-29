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
from typing import Optional, Union

import ujson

from app.translator.core.mapping import SourceMapping
from app.translator.core.mitre import MitreConfig
from app.translator.core.models.parser_output import MetaInfoContainer
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.platforms.elasticsearch.const import ELASTICSEARCH_DETECTION_RULE, elasticsearch_rule_details
from app.translator.platforms.elasticsearch.mapping import ElasticSearchMappings, elasticsearch_mappings
from app.translator.platforms.elasticsearch.renders.elasticsearch import (
    ElasticSearchFieldValue,
    ElasticSearchQueryRender,
)


class ElasticSearchRuleFieldValue(ElasticSearchFieldValue):
    details: PlatformDetails = elasticsearch_rule_details


class ElasticSearchRuleRender(ElasticSearchQueryRender):
    details: PlatformDetails = elasticsearch_rule_details
    mappings: ElasticSearchMappings = elasticsearch_mappings
    mitre: MitreConfig = MitreConfig()

    or_token = "OR"
    and_token = "AND"
    not_token = "NOT"

    field_value_map = ElasticSearchRuleFieldValue(or_token=or_token)
    query_pattern = "{prefix} {query} {functions}"

    def __create_mitre_threat(self, mitre_attack: dict) -> Union[list, list[dict]]:
        if not mitre_attack.get("techniques"):
            return []
        threat = []

        if not mitre_attack.get("tactics"):
            for technique in mitre_attack.get("techniques"):
                technique_name = technique["technique"]
                if "." in technique_name:
                    technique_name = technique_name[: technique_name.index(".")]
                threat.append(technique_name)
            return sorted(threat)

        for tactic in mitre_attack["tactics"]:
            tactic_render = {"id": tactic["external_id"], "name": tactic["tactic"], "reference": tactic["url"]}
            sub_threat = {"tactic": tactic_render, "framework": "MITRE ATT&CK", "technique": []}
            for technique in mitre_attack["techniques"]:
                technique_id = technique["technique_id"].lower()
                if "." in technique_id:
                    technique_id = technique_id[: technique["technique_id"].index(".")]
                main_technique = self.mitre.get_technique(technique_id)
                if tactic["tactic"] in main_technique["tactic"]:
                    sub_threat["technique"].append(
                        {
                            "id": main_technique["technique_id"],
                            "name": main_technique["technique"],
                            "reference": main_technique["url"],
                        }
                    )
            if len(sub_threat["technique"]) > 0:
                threat.append(sub_threat)

        return sorted(threat, key=lambda x: x["tactic"]["id"])

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
        rule = copy.deepcopy(ELASTICSEARCH_DETECTION_RULE)
        description = meta_info.description or rule["description"]

        rule.update(
            {
                "query": query,
                "description": description,
                "name": meta_info.title,
                "rule_id": meta_info.id,
                "author": [meta_info.author],
                "severity": meta_info.severity,
                "references": meta_info.references,
                "license": meta_info.license,
                "tags": meta_info.tags,
                "threat": self.__create_mitre_threat(meta_info.mitre_attack),
                "false_positives": meta_info.false_positives,
            }
        )
        rule_str = ujson.dumps(rule, indent=4, sort_keys=False, ensure_ascii=False)
        if not_supported_functions:
            rendered_not_supported = self.render_not_supported_functions(not_supported_functions)
            return rule_str + rendered_not_supported
        return rule_str
