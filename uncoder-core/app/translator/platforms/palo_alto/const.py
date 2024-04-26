from app.translator.core.models.platform_details import PlatformDetails

PLATFORM_DETAILS = {"group_id": "cortex", "group_name": "Palo Alto Cortex XSIAM"}

CORTEX_XSIAM_XQL_QUERY_DETAILS = {
    "platform_id": "cortex-xql-query",
    "name": "Palo Alto Cortex XSIAM Query",
    "platform_name": "Query (XQL)",
    **PLATFORM_DETAILS,
}

cortex_xql_query_details = PlatformDetails(**CORTEX_XSIAM_XQL_QUERY_DETAILS)
