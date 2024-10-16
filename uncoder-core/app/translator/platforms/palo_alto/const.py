from app.translator.core.custom_types.predefined_fields import IPLocationType, TimeType
from app.translator.core.models.platform_details import PlatformDetails

PLATFORM_DETAILS = {}

CORTEX_XSIAM_XQL_QUERY_DETAILS = {
    "platform_id": "cortex-xql-query",
    "name": "Palo Alto Cortex XSIAM Query",
    "platform_name": "Query (XQL)",
    "group_id": "cortex-xsiam",
    "group_name": "Palo Alto Cortex XSIAM",
}

CORTEX_XDR_XQL_QUERY_DETAILS = {
    "platform_id": "cortex-xdr-xql-query",
    "name": "Palo Alto Cortex XDR Query",
    "platform_name": "Query (XQL)",
    "group_id": "cortex-xdr",
    "group_name": "Palo Alto Cortex XDR",
}

cortex_xsiam_xql_query_details = PlatformDetails(**CORTEX_XSIAM_XQL_QUERY_DETAILS)
cortex_xdr_xql_query_details = PlatformDetails(**CORTEX_XDR_XQL_QUERY_DETAILS)


PREDEFINED_FIELDS_MAP = {
    IPLocationType.asn: "loc_asn",
    IPLocationType.asn_org: "loc_asn_org",
    IPLocationType.city: "loc_city",
    IPLocationType.continent: "loc_continent",
    IPLocationType.country: "loc_country",
    IPLocationType.lat_lon: "loc_latlon",
    IPLocationType.region: "loc_region",
    IPLocationType.timezone: "loc_timezone",
    TimeType.timestamp: "_time",
}
