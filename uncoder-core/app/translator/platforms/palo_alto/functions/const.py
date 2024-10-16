from app.translator.tools.custom_enum import CustomEnum


class CortexXQLFunctionType(CustomEnum):
    avg = "avg"
    count = "count"
    count_distinct = "count_distinct"
    min = "min"
    max = "max"
    sum = "sum"
    values = "values"

    divide = "divide"
    multiply = "multiply"

    lower = "lowercase"
    split = "split"
    upper = "uppercase"

    array_length = "array_length"
    extract_time = "extract_time"
    incidr = "incidr"

    alter = "alter"
    bin = "bin"
    comp = "comp"
    config = "config"
    fields = "fields"
    filter = "filter"
    iploc = "iploc"
    join = "join"
    limit = "limit"
    sort = "sort"
    timeframe = "timeframe"
    timestamp_diff = "timestamp_diff"
    union = "union"


class CortexXQLSortOrderType(CustomEnum):
    asc = "asc"
    desc = "desc"


class CortexXQLTimeFrameType(CustomEnum):
    years = "y"
    months = "mo"
    days = "d"
    hours = "h"
    minutes = "m"
