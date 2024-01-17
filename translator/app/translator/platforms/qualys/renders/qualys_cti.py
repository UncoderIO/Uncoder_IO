from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.render_cti import RenderCTI
from app.translator.platforms.qualys.const import QUALYS_QUERY_DETAILS
from app.translator.platforms.qualys.mappings.qualys_cti import DEFAULT_QUALYS_MAPPING


class QualysCTI(RenderCTI):
    details: PlatformDetails = PlatformDetails(**QUALYS_QUERY_DETAILS)

    field_value_template: str = "{key}:`{value}`"
    or_operator: str = " or "
    group_or_operator: str = " or "
    or_group: str = "({or_group})"
    result_join: str = ""
    final_result_for_many: str = "({result})\n"
    final_result_for_one: str = "{result}\n"
    default_mapping = DEFAULT_QUALYS_MAPPING
