from app.translator.core.models.platform_details import PlatformDetails

ATHENA_QUERY_DETAILS = {
    "platform_id": "athena-sql-query",
    "name": "AWS Athena Query",
    "group_name": "AWS Athena",
    "platform_name": "Query",
    "group_id": "athena",
    "alt_platform_name": "OCSF",
}

athena_query_details = PlatformDetails(**ATHENA_QUERY_DETAILS)
