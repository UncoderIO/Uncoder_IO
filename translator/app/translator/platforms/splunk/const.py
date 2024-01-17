from app.translator.core.models.platform_details import PlatformDetails

DEFAULT_SPLUNK_ALERT = """
[<title_place_holder>]
alert.severity = <severity_place_holder>
description = <description_place_holder>
cron_schedule = 0 * * * *
disabled = 1
is_scheduled = 1
is_visible = 1
dispatch.earliest_time = -60m@m
dispatch.latest_time = now
search = <query_place_holder>
alert.suppress = 0
alert.track = 1
actions = risk,notable
action.risk = 1
action.risk.param._risk_object_type = user
action.risk.param._risk_score = 75
action.correlationsearch = 0
action.correlationsearch.enabled = 1
action.notable.param.rule_title = <title_place_holder>
action.notable.param.rule_description = <description_place_holder>
action.correlationsearch.label = <title_place_holder>
<annotations_place_holder>
"""

PLATFORM_DETAILS = {"group_id": "splunk-pack", "group_name": "Splunk"}

SPLUNK_QUERY_DETAILS = {
    "siem_type": "splunk-spl-query",
    "name": "Splunk Query",
    "platform_name": "Query (SPL)",
    **PLATFORM_DETAILS,
}

SPLUNK_ALERT_DETAILS = {
    "siem_type": "splunk-spl-rule",
    "name": "Splunk Alert",
    "platform_name": "Alert (SPL)",
    "first_choice": 0,
    **PLATFORM_DETAILS,
}

splunk_query_details = PlatformDetails(**SPLUNK_QUERY_DETAILS)
splunk_alert_details = PlatformDetails(**SPLUNK_ALERT_DETAILS)
