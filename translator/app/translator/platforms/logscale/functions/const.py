
from app.translator.tools.custom_enum import CustomEnum


class LogScaleFunctionType(CustomEnum):
    avg = "avg"
    count = "count"
    group_by = "groupBy"
    max = "max"
    min = "min"
    search = "search"
    sort = "sort"
    sum = "sum"
    table = "table"
