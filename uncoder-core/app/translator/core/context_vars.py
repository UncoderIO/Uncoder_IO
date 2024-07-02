from contextvars import ContextVar
from typing import Optional

return_only_first_query_ctx_var: ContextVar[bool] = ContextVar("return_only_first_query_ctx_var", default=False)
"""Set to True to return only first query if rendered multiple options"""

wrap_query_with_meta_info_ctx_var: ContextVar[bool] = ContextVar("wrap_query_with_meta_info_ctx_var", default=True)
"""Set to False not to wrap query with meta info commentary"""

preset_log_source_str_ctx_var: ContextVar[Optional[str]] = ContextVar("preset_log_source_str_ctx_var", default=None)
