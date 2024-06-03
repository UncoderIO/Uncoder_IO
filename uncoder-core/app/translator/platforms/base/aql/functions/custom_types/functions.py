from app.translator.tools.custom_enum import CustomEnum


class AQLFunctionType(CustomEnum):
    lower: str = "LOWER"
    upper: str = "UPPER"
    min: str = "MIN"
    max: str = "MAX"
    sum: str = "SUM"
    avg: str = "AVG"
    count: str = "COUNT"
    distinct_count: str = "DISTINCTCOUNT"
    last: str = "LAST"
    fields: str = "fields"
    aggregation_data_parser: str = "aggregation_data_parser"
