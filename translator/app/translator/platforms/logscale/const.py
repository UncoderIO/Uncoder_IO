from app.translator.core.models.platform_details import PlatformDetails

DEFAULT_LOGSCALE_ALERT = {
    "name": "",
    "query": {"queryString": "", "isLive": True, "start": "1h"},
    "description": "",
    "throttleTimeMillis": 60000,
    "silenced": False,
}

PLATFORM_DETAILS = {"group_id": "logscale-pack", "group_name": "Falcon LogScale"}

LOGSCALE_QUERY_DETAILS = {
    "siem_type": "logscale-lql-query",
    "name": "Falcon LogScale Query",
    "platform_name": "Query",
    **PLATFORM_DETAILS,
}

LOGSCALE_ALERT_DETAILS = {
    "siem_type": "logscale-lql-rule",
    "name": "Falcon LogScale Alert",
    "platform_name": "Alert",
    "first_choice": 0,
    **PLATFORM_DETAILS,
}


logscale_query_details = PlatformDetails(**LOGSCALE_QUERY_DETAILS)
logscale_alert_details = PlatformDetails(**LOGSCALE_ALERT_DETAILS)
