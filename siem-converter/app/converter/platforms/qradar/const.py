from app.converter.core.models.platform_details import PlatformDetails

UTF8_PAYLOAD_PATTERN = r"UTF8\(payload\)"

QRADAR_QUERY_DETAILS = {
    "siem_type": "qradar-aql-query",
    "name": "QRadar Query",
    "platform_name": "Query (AQL)",
    "group_id": "qradar",
    "group_name": "QRadar"
}

NUM_VALUE_PATTERN = r"(?P<num_value>\d+(?:\.\d+)*)"
SINGLE_QUOTES_VALUE_PATTERN = r"""'(?P<s_q_value>(?:[:a-zA-Z\*0-9=+%#\-\/\\,_".$&^@!\(\)\{\}\s]|'')*)'"""


qradar_query_details = PlatformDetails(**QRADAR_QUERY_DETAILS)
