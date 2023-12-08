from app.translator.tools.custom_enum import CustomEnum


class FunctionType(CustomEnum):
    avg = "avg"
    count = "count"
    max = "max"
    min = "min"
    search = "search"
    sort = "sort"
    stats = "stats"
    sum = "sum"
    table = "table"
