from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.render_cti import RenderCTI
from app.translator.managers import render_cti_manager
from app.translator.platforms.arcsight.const import arcsight_query_details, DEFAULT_ARCSIGHT_CTI_MAPPING


@render_cti_manager.register
class ArcsightKeyword(RenderCTI):
    details: PlatformDetails = arcsight_query_details

    default_mapping = DEFAULT_ARCSIGHT_CTI_MAPPING
    field_value_template: str = "{key} = {value}"
    or_operator: str = " OR "
    group_or_operator: str = " OR "
    or_group: str = "{or_group}"
    result_join: str = ""
    final_result_for_many: str = '({result}) AND type != 2 | rex field = flexString1 mode=sed "s//Sigma: None/g"\n'
    final_result_for_one: str = '{result} AND type != 2 | rex field = flexString1 mode=sed "s//Sigma: None/g"\n'
