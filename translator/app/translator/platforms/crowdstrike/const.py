from app.translator.core.models.platform_details import PlatformDetails

CROWDSTRIKE_QUERY_DETAILS = {
    "siem_type": "crowdstrike-spl-query",
    "name": "CrowdStrike Endpoint Security",
    "platform_name": "Query (SPL)",
    "group_id": "crowdstrike",
    "group_name": "CrowdStrike Endpoint Security"
}

crowdstrike_query_details = PlatformDetails(**CROWDSTRIKE_QUERY_DETAILS)
