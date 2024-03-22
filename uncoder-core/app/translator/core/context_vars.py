from contextvars import ContextVar

with_meta_info_annotation_ctx_var: ContextVar[bool] = ContextVar("with_meta_info_annotation_ctx_var", default=False)
"""Set to True to return only the query, excluding meta information and comments."""
