ARCSIGHT_QUERY_DETAILS = {
    "platform_id": "arcsight",
    "name": "ArcSight Query",
    "group_name": "ArcSight",
    "group_id": "arcsight",
    "platform_name": "Query",
    "alt_platform_name": "CEF",
}


DEFAULT_ARCSIGHT_CTI_MAPPING = {
    "SourceIP": "sourceAddress",
    "DestinationIP": "destinationAddress",
    "Domain": "destinationDnsDomain",
    "URL": "requestUrl",
    "HashMd5": "fileHash",
    "HashSha1": "fileHash",
    "HashSha256": "fileHash",
    "HashSha512": "fileHash",
    "Emails": "sender-address",
    "Files": "winlog.event_data.TargetFilename",
}
