FIELD_PATTERN = r"(?P<___group_name___>[a-zA-Z0-9.\-_{}]+)"
DOUBLE_QUOTES_VALUE_PATTERN = r'"(?P<___group_name___>(?:[:a-zA-Z*0-9=+%#\-_/,;`?~‘○×\'.<>$&^@!\]\[(){}\s]|\\\"|\\)*)"'  # noqa: RUF001
SINGLE_QUOTES_VALUE_PATTERN = r"'(?P<___group_name___>(?:[:a-zA-Z*0-9=+%#\-_/,;`?~‘○×\".<>$&^@!\]\[(){}\s]|\\\'|\\)*)'"  # noqa: RUF001
NO_QUOTES_VALUES_PATTERN = (
    r"(?P<___group_name___>(?:[:a-zA-Z*0-9+%#\-_/,.$&^@!]|\\\s|\\=|\\!=|\\<|\\<=|\\>|\\>=|\\\\)+)"
)
NUM_VALUE_PATTERN = r"(?P<___group_name___>\d+(?:\.\d+)?)"
