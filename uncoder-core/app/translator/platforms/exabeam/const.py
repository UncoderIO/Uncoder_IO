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

from app.translator.core.custom_types.meta_info import SeverityType
from app.translator.core.models.platform_details import PlatformDetails

PLATFORM_DETAILS = {"group_id": "exabeam", "group_name": "Exabeam New-Scale", "alt_platform_name": "Default"}

_EXABEAM_EQL_QUERY = "exabeam-eql-query"
_EXABEAM_ANALYTICS_RULE = "exabeam-analytics-rule"
_EXABEAM_CORRELATION_RULE = "exabeam-correlation-rule"

EXABEAM_QUERY_TYPES = {
    _EXABEAM_EQL_QUERY,
    _EXABEAM_ANALYTICS_RULE,
    _EXABEAM_CORRELATION_RULE,
}

EXABEAM_EQL_QUERY_DETAILS = {
    "platform_id": _EXABEAM_EQL_QUERY,
    "name": "Exabeam EQL Query",
    "platform_name": "Search Query (EQL)",
    "file_extension": "txt",
    **PLATFORM_DETAILS,
}

EXABEAM_ANALYTICS_RULE_DETAILS = {
    "platform_id": _EXABEAM_ANALYTICS_RULE,
    "name": "Exabeam Analytics Rule",
    "platform_name": "Analytics Rule (JSON)",
    "file_extension": "json",
    **PLATFORM_DETAILS,
}

EXABEAM_CORRELATION_RULE_DETAILS = {
    "platform_id": _EXABEAM_CORRELATION_RULE,
    "name": "Exabeam Correlation Rule",
    "platform_name": "Correlation Rule (JSON)",
    "file_extension": "json",
    **PLATFORM_DETAILS,
}

exabeam_eql_query_details = PlatformDetails(**EXABEAM_EQL_QUERY_DETAILS)
exabeam_analytics_rule_details = PlatformDetails(**EXABEAM_ANALYTICS_RULE_DETAILS)
exabeam_correlation_rule_details = PlatformDetails(**EXABEAM_CORRELATION_RULE_DETAILS)

EXABEAM_ANALYTICS_RULE_TEMPLATE = {
    "version": "1",
    "ruleDefinitions": [{
        "templateId": "",
        "name": "",
        "description": "",
        "applicableEvents": [{"activity_type": ""}],
        "detectionReason": "",
        "type": "factFeature",
        "mitre": [],
        "useCases": [],
        "value": "true",
        "actOnCondition": "",
        "suppressThreshold": "10 minutes",
        "trainOnCondition": "true",
        "suppressScope": "JoinIfExists(EntityId('type: User && direction: Source'), EntityId('type: Device && direction: Source'))",
        "familyId": "",
        "ruleGroupId": "",
        "severity": "Medium"
    }]
}

EXABEAM_CORRELATION_RULE_TEMPLATE = {
    "version": "1",
    "ruleDefinitions": [{
        "name": "",
        "description": "",
        "useCase": "",
        "mitre": [],
        "sequencesExecution": "CREATION_ORDER",
        "severity": "medium",
        "sequencesConfig": {
            "sequences": [{
                "name": "",
                "query": "",
                "condition": {"triggerOnAnyMatch": True},
                "id": ""
            }],
            "commonProperties": None,
            "outcomes": None
        }
    }]
}

DEFAULT_EXABEAM_CTI_MAPPING = {
    "DestinationIP": "dest_ip",
    "SourceIP": "src_ip", 
    "HashSha512": "file_hash",
    "HashSha256": "file_hash",
    "HashMd5": "file_hash",
    "Emails": "user",
    "Domain": "dest_host",
    "HashSha1": "file_hash",
    "Files": "file_name",
    "URL": "url",
}