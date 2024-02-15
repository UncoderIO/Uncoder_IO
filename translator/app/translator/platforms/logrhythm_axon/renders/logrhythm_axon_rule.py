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
from typing import Optional

from app.translator.core.custom_types.meta_info import SeverityType
from app.translator.core.mapping import SourceMapping
from app.translator.core.models.parser_output import MetaInfoContainer
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.platforms.logrhythm_axon.const import DEFAULT_LOGRHYTHM_AXON_RULE, logrhythm_axon_rule_details
from app.translator.platforms.logrhythm_axon.renders.logrhythm_axon_query import (
    LogRhythmAxonFieldValue,
    LogRhythmAxonQueryRender,
)
from app.translator.tools.utils import get_rule_description_str

_SEVERITIES_MAP = {
    SeverityType.critical: SeverityType.critical,
    SeverityType.high: SeverityType.high,
    SeverityType.medium: SeverityType.medium,
    SeverityType.low: SeverityType.low,
    SeverityType.informational: SeverityType.low,
}


class LogRhythmAxonRuleFieldValue(LogRhythmAxonFieldValue):
    details: PlatformDetails = logrhythm_axon_rule_details


class LogRhythmAxonRuleRender(LogRhythmAxonQueryRender):
    details: PlatformDetails = logrhythm_axon_rule_details
    or_token = "or"
    field_value_map = LogRhythmAxonRuleFieldValue(or_token=or_token)

    def __create_mitre_threat(self, meta_info: MetaInfoContainer) -> tuple[list, list]:
        tactics = set()
        techniques = []

        for tactic in meta_info.mitre_attack.get("tactics"):
            tactics.add(tactic["tactic"])

        for technique in meta_info.mitre_attack.get("techniques"):
            if technique.get("tactic"):
                for tactic in technique["tactic"]:
                    tactics.add(tactic)
            techniques.append(technique["technique_id"])

        return sorted(tactics), sorted(techniques)

    def finalize_query(
        self,
        prefix: str,
        query: str,
        functions: str,
        meta_info: Optional[MetaInfoContainer] = None,
        source_mapping: Optional[SourceMapping] = None,
        not_supported_functions: Optional[list] = None,
        *args,  # noqa: ARG002
        **kwargs,  # noqa: ARG002
    ) -> str:
        query = super().finalize_query(prefix=prefix, query=query, functions=functions)
        rule = copy.deepcopy(DEFAULT_LOGRHYTHM_AXON_RULE)
        rule["observationPipeline"]["pattern"]["operations"][0]["logObserved"]["filter"] = query
        rule["title"] = meta_info.title
        rule["description"] = get_rule_description_str(
            description=meta_info.description or rule["description"],
            author=meta_info.author,
            license_=meta_info.license,
        )
        rule["observationPipeline"]["pattern"]["operations"][0]["ruleElementKey"] = meta_info.id
        rule["observationPipeline"]["metadataFields"]["threat.severity"] = _SEVERITIES_MAP.get(
            meta_info.severity, SeverityType.medium
        )
        if tactics := meta_info.mitre_attack.get("tactics"):
            rule["observationPipeline"]["metadataFields"]["threat.mitre_tactic"] = ", ".join(
                f"{i['external_id']}:{i['tactic']}" for i in tactics
            )
        if techniques := meta_info.mitre_attack.get("techniques"):
            rule["observationPipeline"]["metadataFields"]["threat.mitre_technique"] = ", ".join(
                f"{i['technique_id']}:{i['technique']}" for i in techniques
            )
        if meta_info.fields:
            rule["observationPipeline"]["pattern"]["operations"][0]["logObserved"]["groupByFields"] = [
                self.map_field(field, source_mapping)[0] for field in meta_info.fields
            ]

        json_rule = json.dumps(rule, indent=4, sort_keys=False)
        if not_supported_functions:
            rendered_not_supported = self.render_not_supported_functions(not_supported_functions)
            return json_rule + rendered_not_supported
        return json_rule
