from app.translator.core.custom_types.values import ValueType

UTF8_PAYLOAD_PATTERN = r"UTF8\(payload\)"
NUM_VALUE_PATTERN = rf"(?P<{ValueType.number_value}>\d+(?:\.\d+)*)"
SINGLE_QUOTES_VALUE_PATTERN = rf"""'(?P<{ValueType.single_quotes_value}>(?:[:a-zA-Zа-яА-Я\*0-9=+%#\-\/\\|,;_<>`~".$&^@!?\(\)\{{\}}\[\]\s]|'')*)'"""  # noqa: E501,RUF001
TABLE_PATTERN = r"\s+FROM\s+[a-zA-Z.\-*]+"
TABLE_GROUP_PATTERN = r"\s+FROM\s+(?P<table>[a-zA-Z.\-*]+)"

FIELD_NAME_PATTERN = rf"(?P<{ValueType.no_quotes_value}>[a-zA-Z0-9\._\-]+)"
DOUBLE_QUOTES_FIELD_NAME_PATTERN = rf'"(?P<{ValueType.double_quotes_value}>[a-zA-Z0-9\._\-\s]+)"'
