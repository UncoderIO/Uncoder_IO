from app.translator.core.models.platform_details import PlatformDetails

SIGMA_RULE_DETAILS = {
    "name": "Sigma",
    "platform_id": "sigma",
    "platform_name": "Sigma",
    "group_name": "Sigma",
    "group_id": "sigma",
}

sigma_rule_details = PlatformDetails(**SIGMA_RULE_DETAILS)
