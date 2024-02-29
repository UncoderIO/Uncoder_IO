from app.translator.core.custom_types.meta_info import SeverityType
from app.translator.core.models.platform_details import PlatformDetails

UNMAPPED_FIELD_DEFAULT_NAME = "general_information.raw_message"

DEFAULT_LOGRHYTHM_AXON_RULE = {
    "title": "Default LogRhythm Axon rule",
    "version": 3,
    "description": "Default LogRhythm Axon rule description.",
    "observationPipeline": {
        "pattern": {
            "operations": [
                {
                    "touched": True,
                    "blockType": "LOG_OBSERVED",
                    "logObserved": {"filter": "query", "groupByFields": []},
                    "operationType": "WHERE_PATTERN_OPERATION",
                    "isOutOfBoxRule": False,
                    "ruleElementKey": "rule_id",
                }
            ],
            "afterMatchSkipStrategy": "SKIP_PAST_LAST_EVENT",
        },
        "commonEvents": ["28de4ee0-ca58-40f5-9ac7-ca38edf7883a", "348a37e6-590e-4767-baae-a5c3951391ae"],
        "metadataFields": {"threat.severity": SeverityType.medium},
    },
}

PLATFORM_DETAILS = {"group_id": "axon-ads", "group_name": "LogRhythm Axon"}

LOGRHYTHM_AXON_QUERY_DETAILS = {
    "siem_type": "axon-ads-query",
    "name": "LogRhythm Axon Query",
    "platform_name": "Query",
    **PLATFORM_DETAILS,
}

LOGRHYTHM_AXON_RULE_DETAILS = {
    "siem_type": "axon-ads-rule",
    "name": "LogRhythm Axon Rule",
    "platform_name": "Rule",
    "first_choice": 0,
    **PLATFORM_DETAILS,
}

logrhythm_axon_query_details = PlatformDetails(**LOGRHYTHM_AXON_QUERY_DETAILS)
logrhythm_axon_rule_details = PlatformDetails(**LOGRHYTHM_AXON_RULE_DETAILS)
