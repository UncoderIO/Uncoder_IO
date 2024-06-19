from app.translator.tools.custom_enum import CustomEnum


class SplFunctionType(CustomEnum):
    avg = "avg"
    count = "count"
    distinct_count = "distinct_count"
    earliest = "earliest"
    eval = "eval"
    fields = "fields"
    latest = "latest"
    max = "max"
    min = "min"
    rename = "rename"
    search = "search"
    sort = "sort"
    stats = "stats"
    sum = "sum"
    table = "table"
    values = "values"
    where = "where"


class SplFunctionGroupType(CustomEnum):
    agg = "agg"
    time = "time"


class SplSortOrderType(CustomEnum):
    asc = "+"
    desc = "-"
