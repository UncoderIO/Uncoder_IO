from app.converter.tools.custom_enum import CustomEnum


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
    NEQ = "!="
    COLON = ":"
    CONTAINS = "contains"
    STARTSWITH = "startswith"
    ENDSWITH = "endswith"
    REGEX = "re"
    KEYWORD = "keyword"


class GroupType(CustomEnum):
    L_PAREN = "("
    R_PAREN = ")"
    GROUP = "group"


class ValidTokens(LogicalOperatorType, OperatorType, GroupType):
    pass
