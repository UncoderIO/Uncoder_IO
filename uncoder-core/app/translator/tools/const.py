import typing

IP_IOC_REGEXP_PATTERN = r"(?:^|[ \/\[(\"',;>|])((?:25[0-5]|2[0-4]\d|[0-1]?\d{1,2})(?:\.(?:25[0-5]|2[0-4]\d|[0-1]?\d{1,2})){3})(?=[\s)\]\"',;:\/?\n<|]|$)"  # noqa: E501
DOMAIN_IOC_REGEXP_PATTERN = r"(?:^|[\s\/\[\]@(\"',;{>|])(?:(?:http[s]?|ftp):\/\/?)?([^:\\\/\s({\[\]@\"'`,]+\.[a-zA-Z]+)(?:(?:(?:[/|:]\w+)*\/)(?:[\w\-.]+[^#?\s]+)?(?:[\w/\-&?=%.#]+(?:\(\))?)?)?(?=[\s)\]\"',;<|]|$)"  # noqa: E501
URL_IOC_REGEXP_PATTERN = r"(?:^|[\s\/\[\]@(\"',;{>|])((?:(?:http[s]?|ftp):\/\/?)+(?:[^:\\\/\s({\[\]@\"'`,]+\.[a-zA-Z0-9]+)(?:(?:(?:[/|:]\w+)*\/)(?:[\w\-.]+[^#?\s<']+)?(?:[\w/\-&?=%.#]+(?:\(\))?)?)?)(?=[\s)\]\"',;<|]|$)"  # noqa: E501

IOCType = typing.Literal["ip", "domain", "url", "hash"]
HashType = typing.Literal["md5", "sha1", "sha256", "sha512"]
IocParsingRule = typing.Literal["replace_dots", "remove_private_and_reserved_ips", "replace_hxxp"]

DefaultIOCType = list(typing.get_args(IOCType))
DefaultHashType = list(typing.get_args(HashType))
DefaultIocParsingRule = list(typing.get_args(IocParsingRule))

HASH_MAP = {"md5": "HashMd5", "sha1": "HashSha1", "sha256": "HashSha256", "sha512": "HashSha512"}

iocs_types_map = {
    "url": ["URL"],
    "domain": ["Domain"],
    "ip": ["DestinationIP", "SourceIP"],
    "hash": ["HashMd5", "HashSha1", "HashSha256", "HashSha512"],
}

LOGSOURCE_MAP = {
    "hash": {"category": "process_creation"},
    "domain": {"category": "proxy"},
    "url": {"category": "proxy"},
    "ip": {"category": "proxy"},
    "emails": {"category": "mail"},
    "files": {"category": "file_event"},
}

hash_regexes = {
    "md5": r"(?:^|[\s\/\[(\"',;{>|])([A-Fa-f0-9]{32})(?=[\s)\]\"',;\n<|]|$)",
    "sha1": r"(?:^|[\s\/\[(\"',;{>|])([A-Fa-f0-9]{40})(?=[\s)\]\"',;\n<|]|$)",
    "sha256": r"(?:^|[\s\/\[(\"',;{>|])([A-Fa-f0-9]{64})(?=[\s)\]\"',;\n<|]|$)",
    "sha512": r"(?:^|[\s\/\[(\"',;{>|])([A-Fa-f0-9]{128})(?=[\s)\]\"',;\n<|]|$)",
}
