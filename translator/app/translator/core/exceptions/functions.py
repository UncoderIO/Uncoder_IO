class BaseFunctionException(Exception): ...


class InternalFunctionException(Exception):
    pass


class NotSupportedFunctionException(InternalFunctionException):
    pass


class InvalidFunctionSignature(InternalFunctionException):
    pass
