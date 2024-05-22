from app.translator.core.models.platform_details import PlatformDetails

QRADAR_QUERY_DETAILS = {
    "platform_id": "qradar-aql-query",
    "name": "QRadar Query",
    "platform_name": "Query (AQL)",
    "group_id": "qradar",
    "group_name": "QRadar",
}

qradar_query_details = PlatformDetails(**QRADAR_QUERY_DETAILS)
