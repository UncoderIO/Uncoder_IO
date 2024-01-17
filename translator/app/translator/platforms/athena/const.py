from app.translator.core.models.platform_details import PlatformDetails

ATHENA_QUERY_DETAILS = {
    "siem_type": "athena-sql-query",
    "name": "AWS Athena Query",
    "group_name": "AWS Athena",
    "platform_name": "Query",
    "group_id": "athena",
    "alt_platform_name": "OCSF",
}

athena_details = PlatformDetails(**ATHENA_QUERY_DETAILS)
