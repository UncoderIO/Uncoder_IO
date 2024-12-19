from app.translator.core.custom_types.meta_info import SeverityType
from app.translator.core.models.platform_details import PlatformDetails

UNMAPPED_FIELD_DEFAULT_NAME = "general_information.raw_message"

DEFAULT_LOGRHYTHM_Siem_RULE = {
    "title": "Default LogRhythm Siem rule",
    "version": 1,
    "description": "Default LogRhythm Siem rule description.",
    "maxMsgsToQuery": 30000,
    "logCacheSize": 10000,
    "aggregateLogCacheSize": 10000,
    "queryTimeout": 60,
    "isOriginatedFromWeb": False,
    "webLayoutId": 0,
    "queryRawLog": True,
    "queryFilter": {
        "msgFilterType": 2,
        "isSavedFilter": False,
        "filterGroup": {
            "filterItemType": 1,
            "fieldOperator": 1,
            "filterMode": 1,
            "filterGroupOperator": 0,

            "filterItems":"query",
                "name": "Filter Group",
                # "raw": "query" # FOR DEBUG REASONS
        }
    },
    "queryEventManager": False,
    "useDefaultLogRepositories": True,
    "dateCreated": "2024-06-05T22:47:06.3683942Z",
    "dateSaved": "2024-06-05T22:47:06.3683942Z",
    "dateUsed": "2024-06-05T22:47:06Z",
    "includeDiagnosticEvents": True,
    "searchMode": 2,
    "webResultMode": 0,
    "nextPageToken": "",
    "pagedTimeout": 300,
    "restrictedUserId": 0,
    "createdVia": 0,
    "searchType": 1,
    "queryOrigin": 0,
    "searchServerIPAddress": None,
    "dateCriteria": {
        "useInsertedDate": False,
        "lastIntervalValue": 24,
        "lastIntervalUnit": 7
    },
    "repositoryPattern": "",
    "ownerId": 227,
    "searchId": 0,
    "queryLogSourceLists": [],
    "queryLogSources": [],
    "logRepositoryIds": [],
    "refreshRate": 0,
    "isRealTime": False,
    "objectSecurity": {
        "objectId": 0,
        "objectType": 20,
        "readPermissions": 0,
        "writePermissions": 0,
        "entityId": 1,
        "ownerId": 227,
        "canEdit": True,
        "canDelete": False,
        "canDeleteObject": False,
        "entityName": "",
        "ownerName": "",
        "isSystemObject": True
    },
    "enableIntelligentIndexing": False
}

PLATFORM_DETAILS = {"group_id": "siem-ads", "group_name": "LogRhythm Siem"}

LOGRHYTHM_Siem_QUERY_DETAILS = {
    "platform_id": "siem-ads-query",
    "name": "LogRhythm Siem Query",
    "platform_name": "Query",
    **PLATFORM_DETAILS,
}

LOGRHYTHM_Siem_RULE_DETAILS = {
    "platform_id": "siem-ads-rule",
    "name": "LogRhythm Siem Search API",
    "platform_name": "Search API",
    "first_choice": 0,
    **PLATFORM_DETAILS,
}

# logrhythm_siem_query_details = PlatformDetails(**LOGRHYTHM_Siem_QUERY_DETAILS)
logrhythm_siem_rule_details = PlatformDetails(**LOGRHYTHM_Siem_RULE_DETAILS)
