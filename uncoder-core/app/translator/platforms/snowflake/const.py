SNOWFLAKE_QUERY_DETAILS = {
    "platform_id": "snowflake",
    "name": "Snowflake Query",
    "group_name": "Snowflake",
    "group_id": "snowflake-pack",
    "platform_name": "Query (SQL)",
}

DEFAULT_SNOWFLAKE_CTI_MAPPING = {
    "SourceIP": "source.ip",
    "DestinationIP": "destination.ip",
    "Domain": "destination.domain",
    "URL": "url.original",
    "HashMd5": "file.hash.md5",
    "HashSha1": "file.hash.sha1",
    "HashSha256": "file.hash.sha256",
    "HashSha512": "file.hash.sha512",
    "Files": "file.path",
    "Emails": "user.name",
}
