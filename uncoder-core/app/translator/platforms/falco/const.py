from app.translator.core.models.platform_details import PlatformDetails

FALCO_RULE_DETAILS = {
    "platform_id": "falco-yaml-rule",
    "name": "Falco YAML Rule",
    "platform_name": "Rule (YAML)",
    "group_id": "falco",
    "group_name": "Falco",
}

falco_rule_details = PlatformDetails(**FALCO_RULE_DETAILS)
