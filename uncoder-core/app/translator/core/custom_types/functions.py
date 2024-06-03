from app.translator.tools.custom_enum import CustomEnum


class FunctionType(CustomEnum):
    avg = "avg"
    count = "count"
    distinct_count = "distinct_count"
    max = "max"
    min = "min"
    sum = "sum"

    divide = "divide"

    earliest = "earliest"
    latest = "latest"

    lower = "lower"
    upper = "upper"

    compare_boolean = "compare_boolean"

    ipv4_is_in_range = "ipv4_is_in_range"

    bin = "bin"
    eval = "eval"
    fields = "fields"
    rename = "rename"
    search = "search"
    sort_limit = "sort_limit"
    stats = "stats"
    table = "table"
    timeframe = "timeframe"
    values = "values"
