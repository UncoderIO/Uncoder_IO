from app.translator.core.models.platform_details import PlatformDetails

CARBON_BLACK_QUERY_DETAILS = {
    "platform_id": "carbonblack",
    "name": "Carbon Black Cloud",
    "group_name": "VMware Carbon Black",
    "group_id": "carbonblack-pack",
    "platform_name": "Query (Cloud)",
}

DEFAULT_CARBONBLACK_CTI_MAPPING = {
    "SourceIP": "netconn_local_ipv4",
    "DestinationIP": "netconn_ipv4",
    "Domain": "netconn_domain",
    "URL": "netconn_domain",
    "HashMd5": "hash",
    "HashSha256": "hash",
    "Files": "filemod_name",
    "Emails": "process_username",
}


carbonblack_query_details = PlatformDetails(**CARBON_BLACK_QUERY_DETAILS)
