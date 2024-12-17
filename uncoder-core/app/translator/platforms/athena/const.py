from app.translator.core.models.platform_details import PlatformDetails

ATHENA_QUERY_DETAILS = {
    "platform_id": "athena-sql-query",
    "name": "AWS Athena Query",
    "group_name": "AWS Athena",
    "platform_name": "Query",
    "group_id": "athena",
    "alt_platform_name": "OCSF",
}

DEFAULT_ATHENA_CTI_MAPPING = {
    "SourceIP": "src_endpoint",
    "DestinationIP": "dst_endpoint",
    "Domain": "dst_endpoint",
    "URL": "http_request",
    "HashMd5": "unmapped.file.hash.md5",
    "HashSha1": "unmapped.file.hash.sha1",
    "HashSha256": "unmapped.file.hash.sha256",
    "HashSha512": "unmapped.file.hash.sha512",
    "Email": "email",
    "FileName": "file.name",
}


athena_query_details = PlatformDetails(**ATHENA_QUERY_DETAILS)
