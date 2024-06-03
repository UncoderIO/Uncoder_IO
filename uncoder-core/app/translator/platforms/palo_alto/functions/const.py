from app.translator.tools.custom_enum import CustomEnum


class CortexXQLFunctionType(CustomEnum):
    avg = "avg"
    count = "count"
    count_distinct = "count_distinct"
    min = "min"
    max = "max"
    sum = "sum"

    divide = "divide"

    lower = "lowercase"
    upper = "uppercase"

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


class XqlSortOrderType(CustomEnum):
    asc = "asc"
    desc = "desc"


class XqlTimeFrameType(CustomEnum):
    days = "d"
    hours = "h"
    minutes = "m"


class XqlSpanType(CustomEnum):
    days = "d"
    hours = "h"
    minutes = "m"
