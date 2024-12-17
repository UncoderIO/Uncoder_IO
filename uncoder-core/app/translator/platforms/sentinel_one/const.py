from app.translator.core.models.platform_details import PlatformDetails

PLATFORM_DETAILS = {"group_id": "sentinel-one", "group_name": "SentinelOne"}

SENTINEL_ONE_EVENTS_QUERY_DETAILS = {
    "platform_id": "s1-events",
    "name": "SentinelOne Events Query",
    "platform_name": "Query (Events)",
    **PLATFORM_DETAILS,
}

SENTINEL_ONE_POWER_QUERY_DETAILS = {
    "platform_id": "sentinel-one-power-query",
    "name": "SentinelOne Power Query",
    "platform_name": "Power Query",
    **PLATFORM_DETAILS,
}

DEFAULT_S1EVENTS_CTI_MAPPING = {
    "SourceIP": "SrcIP",
    "DestinationIP": "DstIP",
    "Domain": "DNS",
    "URL": "Url",
    "HashMd5": "Md5",
    "HashSha1": "Sha1",
    "HashSha256": "Sha256",
    "HashSha512": "Sha512",
    "Emails": "emails",
    "Files": "TgtFilePath",
}

sentinel_one_events_query_details = PlatformDetails(**SENTINEL_ONE_EVENTS_QUERY_DETAILS)
sentinel_one_power_query_details = PlatformDetails(**SENTINEL_ONE_POWER_QUERY_DETAILS)
