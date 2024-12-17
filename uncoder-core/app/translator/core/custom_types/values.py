from app.translator.tools.custom_enum import CustomEnum


class ValueType(CustomEnum):
    value = "value"
    number_value = "num_value"
    double_quotes_value = "d_q_value"
    single_quotes_value = "s_q_value"
    back_quotes_value = "b_q_value"
    no_quotes_value = "no_q_value"
    bool_value = "bool_value"
    regex_value = "re_value"
    gte_value = "gte_value"
    lte_value = "lte_value"
    multi_value = "multi_value"
    ip_value = "ip_value"
