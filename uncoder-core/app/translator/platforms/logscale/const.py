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
    "platform_id": "logscale-lql-query",
    "name": "Falcon LogScale Query",
    "platform_name": "Query",
    **PLATFORM_DETAILS,
}

LOGSCALE_ALERT_DETAILS = {
    "platform_id": "logscale-lql-rule",
    "name": "Falcon LogScale Alert",
    "platform_name": "Alert",
    "first_choice": 0,
    **PLATFORM_DETAILS,
}

DEFAULT_LOGSCALE_CTI_MAPPING = {
    "DestinationIP": "dst_ip",
    "SourceIP": "src_ip",
    "HashSha512": "file.hash.sha512",
    "HashSha256": "file.hash.sha256",
    "HashMd5": "file.hash.md5",
    "Emails": "email",
    "Domain": "host",
    "HashSha1": "file.hash.sha1",
    "Files": "winlog.event_data.TargetFilename",
    "URL": "url",
}


logscale_query_details = PlatformDetails(**LOGSCALE_QUERY_DETAILS)
logscale_alert_details = PlatformDetails(**LOGSCALE_ALERT_DETAILS)
