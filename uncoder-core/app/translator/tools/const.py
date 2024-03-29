from typing import Literal

IP_IOC_REGEXP_PATTERN = r"(?:^|[ \/\[(\"',;>|])((?:25[0-5]|2[0-4]\d|[0-1]?\d{1,2})(?:\.(?:25[0-5]|2[0-4]\d|[0-1]?\d{1,2})){3})(?=[\s)\]\"',;:\/?\n<|]|$)"  # noqa: E501
DOMAIN_IOC_REGEXP_PATTERN = r"(?:^|[\s\/\[\]@(\"',;{>|])(?:(?:http[s]?|ftp):\/\/?)?([^:\\\/\s({\[\]@\"'`,]+\.[a-zA-Z]+)(?:(?:(?:[/|:]\w+)*\/)(?:[\w\-.]+[^#?\s]+)?(?:[\w/\-&?=%.#]+(?:\(\))?)?)?(?=[\s)\]\"',;<|]|$)"  # noqa: E501
URL_IOC_REGEXP_PATTERN = r"(?:^|[\s\/\[\]@(\"',;{>|])((?:(?:http[s]?|ftp):\/\/?)+(?:[^:\\\/\s({\[\]@\"'`,]+\.[a-zA-Z0-9]+)(?:(?:(?:[/|:]\w+)*\/)(?:[\w\-.]+[^#?\s<']+)?(?:[\w/\-&?=%.#]+(?:\(\))?)?)?)(?=[\s)\]\"',;<|]|$)"  # noqa: E501

IOCType = Literal["ip", "domain", "url", "hash"]
HashType = Literal["md5", "sha1", "sha256", "sha512"]
IocParsingRule = Literal["replace_dots", "remove_private_and_reserved_ips", "replace_hxxp"]

HASH_MAP = {"md5": "HashMd5", "sha1": "HashSha1", "sha256": "HashSha256", "sha512": "HashSha512"}

hash_regexes = {
    "md5": r"(?:^|[\s\/\[(\"',;{>|])([A-Fa-f0-9]{32})(?=[\s)\]\"',;\n<|]|$)",
    "sha1": r"(?:^|[\s\/\[(\"',;{>|])([A-Fa-f0-9]{40})(?=[\s)\]\"',;\n<|]|$)",
    "sha256": r"(?:^|[\s\/\[(\"',;{>|])([A-Fa-f0-9]{64})(?=[\s)\]\"',;\n<|]|$)",
    "sha512": r"(?:^|[\s\/\[(\"',;{>|])([A-Fa-f0-9]{128})(?=[\s)\]\"',;\n<|]|$)",
}
