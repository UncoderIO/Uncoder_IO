from app.translator.core.models.platform_details import PlatformDetails

CROWDSTRIKE_QUERY_DETAILS = {
    "platform_id": "crowdstrike-spl-query",
    "name": "CrowdStrike Endpoint Security",
    "platform_name": "Query (SPL)",
    "group_id": "crowdstrike",
    "group_name": "CrowdStrike Endpoint Security",
}

DEFAULT_CROWDSTRIKE_CTI_MAPPING = {
    "DestinationIP": "RemoteAddressIP4",
    "SourceIP": "LocalAddressIP4",
    "HashSha256": "SHA256HashData",
    "HashMd5": "MD5HashData",
    "Emails": "emails",
    "Domain": "DomainName",
    "HashSha1": "SHA1HashData",
    "Files": "TargetFileName",
    "URL": "HttpUrl",
}


crowdstrike_query_details = PlatformDetails(**CROWDSTRIKE_QUERY_DETAILS)
