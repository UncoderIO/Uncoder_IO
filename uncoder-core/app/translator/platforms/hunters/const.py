from app.translator.core.models.platform_details import PlatformDetails

HUNTERS_QUERY_DETAILS = {
    "platform_id": "hunters-sql-query",
    "name": "Hunters Query",
    "group_name": "Hunters",
    "platform_name": "Query",
    "group_id": "hunters",
}

hunters_details = PlatformDetails(**HUNTERS_QUERY_DETAILS)
