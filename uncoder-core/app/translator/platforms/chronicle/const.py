from app.translator.core.models.platform_details import PlatformDetails

DEFAULT_CHRONICLE_SECURITY_RULE = """rule <title_place_holder> {
 meta:
    author = "<author_place_holder>"
    description = "<description_place_holder>"
    license = "<licence_place_holder>"
    version = "0.01"
    rule_id = "<rule_id_place_holder>"
    status = "<status_place_holder>"
    tags = "<tags_place_holder>"
    falsepositives = "<falsepositives_place_holder>"
    severity = "<severity_place_holder>"
    created = "<created_place_holder>"

  events:
    <query_placeholder>

  condition:
    $e
}"""

PLATFORM_DETAILS = {"group_id": "chronicle-pack", "group_name": "Google SecOps", "alt_platform_name": "UDM"}

CHRONICLE_QUERY_DETAILS = {
    "platform_id": "chronicle-yaral-query",
    "name": "Google SecOps Query",
    "platform_name": "Query (UDM)",
    **PLATFORM_DETAILS,
}

CHRONICLE_RULE_DETAILS = {
    "platform_id": "chronicle-yaral-rule",
    "name": "Google SecOps Rule",
    "platform_name": "Rule (YARA-L)",
    "first_choice": 0,
    **PLATFORM_DETAILS,
}

chronicle_query_details = PlatformDetails(**CHRONICLE_QUERY_DETAILS)
chronicle_rule_details = PlatformDetails(**CHRONICLE_RULE_DETAILS)
