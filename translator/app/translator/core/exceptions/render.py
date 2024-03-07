class BaseRenderException(BaseException): ...


class UnexpectedLogsourceException(BaseRenderException):
    def __init__(self, platform_name: str, log_source: str):
        message = f"{platform_name} can't convert query with logsources: {log_source}"
        super().__init__(message)


class FunctionRenderException(BaseRenderException): ...


class UnsupportedRenderMethod(BaseRenderException):
    def __init__(self, platform_name: str, method: str):
        message = f"Cannot translate. {platform_name} backend does not support {method}."
        super().__init__(message)
