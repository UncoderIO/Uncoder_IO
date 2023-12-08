from app.translator.core.models.platform_details import PlatformDetails

CROWDSTRIKE_QUERY_DETAILS = {
    "siem_type": "crowdstrike-spl-query",
    "name": "CrowdStrike",
    "platform_name": "Query (SPL)",
    "group_id": "crowdstrike",
    "group_name": "CrowdStrike"
}

crowdstrike_query_details = PlatformDetails(**CROWDSTRIKE_QUERY_DETAILS)
