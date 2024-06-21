from app.translator.tools.custom_enum import CustomEnum


class FunctionType(CustomEnum):
    avg = "avg"
    count = "count"
    distinct_count = "distinct_count"
    max = "max"
    min = "min"
    sum = "sum"

    values = "values"

    earliest = "earliest"
    latest = "latest"

    divide = "divide"

    lower = "lower"
    split = "split"
    upper = "upper"

    array_length = "array_length"
    compare = "compare"
    extract_time = "extract_time"
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
    union = "union"

    aggregation_data_function = "aggregation_data_function"
