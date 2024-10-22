from app.translator.core.custom_types.values import ValueType


class KQLValueType(ValueType):
    verbatim_double_quotes_value = "v_d_q_value"
    verbatim_single_quotes_value = "v_s_q_value"

    double_quotes_regex_value = "double_quotes_re_value"
    single_quotes_regex_value = "single_quotes_re_value"
    verbatim_double_quotes_regex_value = "verbatim_double_quotes_re_value"
    verbatim_single_quotes_regex_value = "verbatim_single_quotes_re_value"
