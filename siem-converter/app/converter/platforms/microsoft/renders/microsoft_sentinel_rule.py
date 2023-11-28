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

from app.converter.platforms.microsoft.renders.microsoft_sentinel import (
    MicrosoftSentinelQueryRender,
    MicrosoftSentinelFieldValue
)
from app.converter.platforms.microsoft.const import DEFAULT_MICROSOFT_SENTINEL_RULE, microsoft_sentinel_rule_details
from app.converter.core.mapping import SourceMapping
from app.converter.core.models.platform_details import PlatformDetails
from app.converter.core.models.parser_output import MetaInfoContainer
from app.converter.tools.utils import concatenate_str, get_author_str, get_licence_str


class MicrosoftSentinelRuleFieldValue(MicrosoftSentinelFieldValue):
    details: PlatformDetails = microsoft_sentinel_rule_details


class MicrosoftSentinelRuleRender(MicrosoftSentinelQueryRender):
    details: PlatformDetails = microsoft_sentinel_rule_details
    or_token = "or"
    field_value_map = MicrosoftSentinelRuleFieldValue(or_token=or_token)

    def finalize_query(self, prefix: str, query: str, functions: str, meta_info: MetaInfoContainer,
                       source_mapping: SourceMapping = None, not_supported_functions: list = None):
        query = super().finalize_query(prefix=prefix, query=query, functions=functions, meta_info=meta_info)
        rule = copy.deepcopy(DEFAULT_MICROSOFT_SENTINEL_RULE)
        rule["query"] = query
        rule["displayName"] = meta_info.title
        description = meta_info.description or rule["description"]
        description = concatenate_str(description, get_author_str(meta_info.author))
        description = concatenate_str(description, get_licence_str(meta_info.license))
        rule["description"] = description
        rule["severity"] = meta_info.severity
        rule["techniques"] = [el.upper() for el in meta_info.mitre_attack]
        json_rule = json.dumps(rule, indent=4, sort_keys=False)
        if not_supported_functions:
            rendered_not_supported = self.render_not_supported_functions(not_supported_functions)
            return json_rule + rendered_not_supported
        return json_rule
