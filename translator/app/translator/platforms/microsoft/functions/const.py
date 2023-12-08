from app.translator.tools.custom_enum import CustomEnum


class KQLFunctionType(CustomEnum):
    avg = "avg"
    count = "count"
    max = "max"
    min = "min"
    sum = "sum"
    where = "where"
    search = "search"
    summarize = "summarize"
    project = "project"
    sort = "sort"
