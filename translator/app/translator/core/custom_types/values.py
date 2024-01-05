from app.translator.tools.custom_enum import CustomEnum


class ValueType(CustomEnum):
    value = "value"
    number_value = "num_value"
    double_quotes_value = "d_q_value"
    single_quotes_value = "s_q_value"
    back_quotes_value = "b_q_value"
    no_quotes_value = "no_q_value"
    bool_value = "bool_value"
    regular_expression_value = "re_value"
    greater_than_or_equal = "gte_value"
    less_than_or_equal = "lte_value"
