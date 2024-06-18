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
    limit = "limit"
    sort = "sort"
    timeframe = "timeframe"
    union = "union"

    compare = "compare"


class XqlSortOrderType(CustomEnum):
    asc = "asc"
    desc = "desc"


class XqlTimeFrameType(CustomEnum):
    years = "y"
    months = "mo"
    days = "d"
    hours = "h"
    minutes = "m"
