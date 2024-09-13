from app.translator.core.models.platform_details import PlatformDetails

ANOMALI_QUERY_DETAILS = {
    "platform_id": "anomali-aql-query",
    "name": "Anomali Security Analytics Query",
    "group_name": "Anomali Security Analytics",
    "platform_name": "Query",
    "group_id": "anomali",
}

anomali_query_details = PlatformDetails(**ANOMALI_QUERY_DETAILS)
