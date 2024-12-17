from app.translator.core.models.platform_details import PlatformDetails

QRADAR_QUERY_DETAILS = {
    "platform_id": "qradar-aql-query",
    "name": "QRadar Query",
    "platform_name": "Query (AQL)",
    "group_id": "qradar",
    "group_name": "QRadar",
}

DEFAULT_QRADAR_CTI_MAPPING = {
    "DestinationIP": "destinationip",
    "SourceIP": "sourceip",
    "HashSha512": "File Hash",
    "HashSha256": "File Hash",
    "HashMd5": "File Hash",
    "Emails": "emails",
    "Domain": "Hostname",
    "HashSha1": "File Hash",
    "Files": "Filename",
    "URL": "URL",
}


qradar_query_details = PlatformDetails(**QRADAR_QUERY_DETAILS)
