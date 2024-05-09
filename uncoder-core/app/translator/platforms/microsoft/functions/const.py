from app.translator.tools.custom_enum import CustomEnum


class KQLFunctionType(CustomEnum):
    avg = "avg"
    count = "count"
    distinct = "distinct"
    distinct_count = "count_distinct"
    extend = "extend"
    max = "max"
    min = "min"
    project = "project"
    project_rename = "project-rename"
    search = "search"
    sort = "sort"
    sum = "sum"
    summarize = "summarize"
    top = "top"
    where = "where"


class KQLSortOrderType(CustomEnum):
    asc = "asc"
    desc = "desc"
