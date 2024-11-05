from app.translator.core.models.platform_details import PlatformDetails

ARCSIGHT_QUERY_DETAILS = {
    "platform_id": "arcsight-query",
    "name": "ArcSight Query",
    "group_name": "ArcSight",
    "group_id": "arcsight",
    "platform_name": "Query",
    "alt_platform_name": "CEF",
}

arcsight_query_details = PlatformDetails(**ARCSIGHT_QUERY_DETAILS)
