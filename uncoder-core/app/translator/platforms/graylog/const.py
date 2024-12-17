from app.translator.core.models.platform_details import PlatformDetails

GRAYLOG_QUERY_DETAILS = {
    "platform_id": "graylog-lucene-query",
    "name": "Graylog",
    "group_name": "Graylog",
    "platform_name": "Query",
    "group_id": "graylog",
}

DEFAULT_GRAYLOG_CTI_MAPPING = {
    "SourceIP": "source.ip",
    "DestinationIP": "destination.ip",
    "Domain": "destination.domain",
    "URL": "url.original",
    "HashMd5": "file.hash.md5",
    "HashSha1": "file.hash.sha1",
    "HashSha256": "file.hash.sha256",
    "HashSha512": "file.hash.sha512",
    "Emails": "emails",
    "Files": "filePath",
}


graylog_query_details = PlatformDetails(**GRAYLOG_QUERY_DETAILS)
