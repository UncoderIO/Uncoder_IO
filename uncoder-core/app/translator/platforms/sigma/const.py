from app.translator.core.models.platform_details import PlatformDetails

SIGMA_RULE_DETAILS = {
    "name": "Sigma",
    "platform_id": "sigma",
    "platform_name": "Sigma",
    "group_name": "Sigma",
    "group_id": "sigma",
}

DEFAULT_SIGMA_CTI_MAPPING = {
    "SourceIP": "SourceIP",
    "DestinationIP": "DestinationIP",
    "Domain": "Domain",
    "URL": "URL",
    "HashMd5": "HashMd5",
    "HashSha1": "HashSha1",
    "HashSha256": "HashSha256",
    "HashSha512": "HashSha512",
}


sigma_rule_details = PlatformDetails(**SIGMA_RULE_DETAILS)
