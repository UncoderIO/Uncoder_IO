
class BaseParserException(BaseException):
    ...


class TokenizerGeneralException(BaseParserException):

    def __init__(self, error: str):
        message = f"It looks like there's been an issue during translation. {error}. Resolve the issue and try again. If you think there's no issue, please contact us. We are improving the translation capabilities for this language, and some operators may be not supported yet."
        super().__init__(message)


class UnsupportedOperatorException(BaseParserException):

    def __init__(self, operator: str):
        message = f"Cannot translate. Operator {operator} is not supported."
        super().__init__(message)


class QueryParenthesesException(BaseParserException):
    def __init__(self):
        message = f"The query logic is broken. In the input, the numbers of opening and closing parentheses do not match. If you think there's no error, please contact us via GitHub."
        super().__init__(message)


class FieldMappingException(BaseParserException):
    def __init__(self, field_name: str):
        message = f"Cannot translate. The field {field_name} does not exist in the output language or its translation is not supported yet. If you want to contribute to the open-source translation capabilities into this language, do it via our UncoderIO GitHub project."
        super().__init__(message)


class FunctionParseException(BaseParserException):
    ...
    # def __init__(self, message: str):
    #     self.message = message