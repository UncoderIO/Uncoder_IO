from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.render_cti import RenderCTI
from app.translator.managers import render_cti_manager
from app.translator.platforms.arcsight.const import ARCSIGHT_QUERY_DETAILS, DEFAULT_ARCSIGHT_CTI_MAPPING


@render_cti_manager.register
class ArcsightKeyword(RenderCTI):
    details: PlatformDetails = PlatformDetails(**ARCSIGHT_QUERY_DETAILS)

    default_mapping = DEFAULT_ARCSIGHT_CTI_MAPPING
    field_value_template: str = "{key} = {value}"
    or_operator: str = " OR "
    group_or_operator: str = " OR "
    or_group: str = "{or_group}"
    result_join: str = ""
    final_result_for_many: str = '({result}) AND type != 2 | rex field = flexString1 mode=sed "s//Sigma: None/g"\n'
    final_result_for_one: str = '{result} AND type != 2 | rex field = flexString1 mode=sed "s//Sigma: None/g"\n'
