SECURONIX_QUERY_DETAILS = {
    "platform_id": "securonix",
    "name": "Securonix",
    "platform_name": "Query",
    "group_name": "Securonix",
    "group_id": "securonix",
}

DEFAULT_SECURONIX_CTI_MAPPING = {
    "DestinationIP": "@destinationaddress",
    "SourceIP": "@sourceaddress",
    "HashSha512": "@filehash",
    "HashSha256": "@filehash",
    "HashMd5": "@filehash",
    "Emails": "emails",
    "Domain": "@destinationhostname",
    "HashSha1": "@filehash",
    "Files": "@filename",
    "URL": "@requesturl",
}
