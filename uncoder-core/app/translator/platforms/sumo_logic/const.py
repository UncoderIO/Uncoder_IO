SUMO_LOGIC_QUERY_DETAILS = {
    "platform_id": "sumologic",
    "name": "Sumo Logic Query",
    "group_name": "Sumo Logic",
    "platform_name": "Query",
    "first_choice": 0,
    "group_id": "sumologic",
}

DEFAULT_SUMOLOGIC_CTI_MAPPING = {
    "SourceIP": "src_ip",
    "DestinationIP": "dst_ip",
    "Domain": "host",
    "URL": "url",
    "HashMd5": "fileHash",
    "HashSha1": "fileHash",
    "HashSha256": "fileHash",
    "HashSha512": "fileHash",
    "Emails": "flattened_destinations",
    "Files": "files",
}
