from app.translator.tools.custom_enum import CustomEnum


class LogicalOperatorType(CustomEnum):
    AND = "and"
    OR = "or"
    NOT = "not"


class OperatorType(CustomEnum):
    LT = "<"
    LTE = "<="
    GT = ">"
    GTE = ">="
    EQ = "="
    NOT_EQ = "!="
    CONTAINS = "contains"
    NOT_CONTAINS = "not contains"
    STARTSWITH = "startswith"
    NOT_STARTSWITH = "not startswith"
    ENDSWITH = "endswith"
    NOT_ENDSWITH = "not endswith"
    REGEX = "re"
    NOT_REGEX = "not re"
    KEYWORD = "keyword"
    IS_NONE = "is none"
    IS_NOT_NONE = "is not none"


class GroupType(CustomEnum):
    L_PAREN = "("
    R_PAREN = ")"
