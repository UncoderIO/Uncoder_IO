from contextvars import ContextVar

return_only_first_query_ctx_var: ContextVar[bool] = ContextVar("return_only_first_query_ctx_var", default=False)
"""Set to True to return only first query if rendered multiple options"""
