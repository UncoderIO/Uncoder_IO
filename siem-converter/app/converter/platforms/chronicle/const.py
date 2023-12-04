from app.converter.core.models.platform_details import PlatformDetails

DEFAULT_CHRONICLE_SECURITY_RULE = """rule <title_place_holder> {
 meta:
    description = "<description_place_holder>"
    license = "<licence_place_holder>"
    version = "0.01"
    rule_id = "<rule_id_place_holder>"
    status = "<status_place_holder>"
    severity = "<severity_place_holder>"
    falsepositives = "<falsepositives_place_holder>"

  events:
    <query_placeholder>

  condition:
    $e
}"""

PLATFORM_DETAILS = {
    "group_id": "chronicle-pack",
    "group_name": "Chronicle Security",
    "alt_platform_name": "UDM"
}

CHRONICLE_QUERY_DETAILS = {
    "siem_type": "chronicle-yaral-query",
    "name": "Chronicle Security Query",
    "platform_name": "Query (UDM)",
    **PLATFORM_DETAILS
}

CHRONICLE_RULE_DETAILS = {
    "siem_type": "chronicle-yaral-rule",
    "name": "Chronicle Security Rule",
    "platform_name": "Rule (YARA-L)",
    "first_choice": 0,
    **PLATFORM_DETAILS
}

chronicle_query_details = PlatformDetails(**CHRONICLE_QUERY_DETAILS)
chronicle_rule_details = PlatformDetails(**CHRONICLE_RULE_DETAILS)
