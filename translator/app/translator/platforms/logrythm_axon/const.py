from app.translator.core.custom_types.meta_info import SeverityType
from app.translator.core.models.platform_details import PlatformDetails

DEFAULT_LOGRYTHM_AXON_RULE = {
    "title": "Default LogrythmAxon rule",
    "version": 3,
    "description": "Default LogrythmAxon rule description.",
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

PLATFORM_DETAILS = {"group_id": "axon-ads", "group_name": "LogRythm Axon"}

LOGRYTHM_AXON_QUERY_DETAILS = {
    "siem_type": "axon-ads-query",
    "name": "LogRythm Axon Query",
    "platform_name": "LogRythm Axon",
    **PLATFORM_DETAILS,
}

LOGRYTHM_AXON_RULE_DETAILS = {
    "siem_type": "axon-ads-rule",
    "name": "LogRythm Axon Rule",
    "platform_name": "LogRythm Axon",
    "first_choice": 0,
    **PLATFORM_DETAILS,
}

logrythm_axon_query_details = PlatformDetails(**LOGRYTHM_AXON_QUERY_DETAILS)
logrythm_axon_rule_details = PlatformDetails(**LOGRYTHM_AXON_RULE_DETAILS)
