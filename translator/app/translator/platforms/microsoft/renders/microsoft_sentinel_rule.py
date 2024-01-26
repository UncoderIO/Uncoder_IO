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
from app.translator.platforms.microsoft.const import DEFAULT_MICROSOFT_SENTINEL_RULE, microsoft_sentinel_rule_details
from app.translator.platforms.microsoft.renders.microsoft_sentinel import (
    MicrosoftSentinelFieldValue,
    MicrosoftSentinelQueryRender,
)
from app.translator.tools.utils import get_rule_description_str

_SEVERITIES_MAP = {
    SeverityType.critical: SeverityType.high,
    SeverityType.high: SeverityType.high,
    SeverityType.medium: SeverityType.medium,
    SeverityType.low: SeverityType.low,
}


class MicrosoftSentinelRuleFieldValue(MicrosoftSentinelFieldValue):
    details: PlatformDetails = microsoft_sentinel_rule_details


class MicrosoftSentinelRuleRender(MicrosoftSentinelQueryRender):
    details: PlatformDetails = microsoft_sentinel_rule_details
    or_token = "or"
    field_value_map = MicrosoftSentinelRuleFieldValue(or_token=or_token)

    def __create_mitre_threat(self, meta_info: MetaInfoContainer) -> tuple[list, list]:
        tactics = []
        techniques = []

        for tactic in meta_info.mitre_attack.get("tactics", []):
            tactics.append(tactic["tactic"])

        for technique in meta_info.mitre_attack.get("techniques", []):
            techniques.append(technique["technique_id"])

        return tactics, techniques

    def finalize_query(
        self,
        prefix: str,
        query: str,
        functions: str,
        meta_info: Optional[MetaInfoContainer] = None,
        source_mapping: Optional[SourceMapping] = None,  # noqa: ARG002
        not_supported_functions: Optional[list] = None,
    ) -> str:
        query = super().finalize_query(prefix=prefix, query=query, functions=functions)
        rule = copy.deepcopy(DEFAULT_MICROSOFT_SENTINEL_RULE)
        rule["query"] = query
        rule["displayName"] = meta_info.title
        rule["description"] = get_rule_description_str(
            description=meta_info.description or rule["description"],
            author=meta_info.author,
            license_=meta_info.license,
        )
        rule["severity"] = _SEVERITIES_MAP.get(meta_info.severity, SeverityType.medium)
        mitre_tactics, mitre_techniques = self.__create_mitre_threat(meta_info=meta_info)
        rule["tactics"] = mitre_tactics
        rule["techniques"] = mitre_techniques
        json_rule = json.dumps(rule, indent=4, sort_keys=False)
        if not_supported_functions:
            rendered_not_supported = self.render_not_supported_functions(not_supported_functions)
            return json_rule + rendered_not_supported
        return json_rule
