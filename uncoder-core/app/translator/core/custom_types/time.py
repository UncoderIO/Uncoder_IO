from app.translator.tools.custom_enum import CustomEnum


class TimeFrameType(CustomEnum):
    years = "years"
    months = "months"
    days = "days"
    hours = "hours"
    minutes = "minutes"


class TimePartType(CustomEnum):
    day = "day"
    day_of_week = "day_of_week"
    day_of_year = "day_of_year"
    hour = "hour"
    microsecond = "microsecond"
    millisecond = "millisecond"
    minute = "minute"
    month = "month"
    quarter = "quarter"
    second = "second"
    year = "year"
