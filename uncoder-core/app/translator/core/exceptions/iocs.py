class BaseIOCsException(BaseException): ...


class IocsLimitExceededException(BaseIOCsException): ...


class EmptyIOCSException(BaseIOCsException):
    def __init__(self):
        message = "No Indicators of Compromise recognized in the input."
        super().__init__(message)
