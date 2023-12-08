from typing import Optional, List
from fastapi import APIRouter, Body

from app.translator.tools.const import IOCType, HashType, IocParsingRule
from app.translator.cti_translator import CTIConverter
from app.models.ioc_translation import CTIPlatform, OneTranslationCTIData
from app.models.translation import InfoMessage

iocs_router = APIRouter()
converter = CTIConverter()


@iocs_router.post(
    "/iocs/translate",
    description="Parse IOCs from text.",
)
@iocs_router.post("/iocs/translate", include_in_schema=False)
def parse_and_translate_iocs(
    text: str = Body(..., description="Text to parse IOCs from", embed=True),
    iocs_per_query: int = Body(25, description="Platforms to parse IOCs to", embed=True),
    platform: CTIPlatform = Body(..., description="Platforms to parse IOCs to", embed=True),
    include_ioc_types: Optional[List[IOCType]] = Body(
        None, description="List of IOC types to include. By default all types are enabled.", embed=True),
    include_hash_types: Optional[List[HashType]] = Body(
        None, description="List of hash types to include. By default all hash types are enabled.", embed=True),
    exceptions: Optional[List[str]] = Body(
        None, description="List of exceptions. IOC is ignored if it contains one of exception values.", embed=True),
    ioc_parsing_rules: Optional[List[IocParsingRule]] = Body(
        None, embed=True, description="Additional parsing parameters."),
    include_source_ip: Optional[bool] = Body(
        False, description="Include source IP in query. By default it is false."
    )
) -> OneTranslationCTIData:
    status, translations = converter.convert(text=text,
                                             platform_data=platform,
                                             iocs_per_query=iocs_per_query,
                                             include_ioc_types=include_ioc_types,
                                             include_hash_types=include_hash_types,
                                             exceptions=exceptions,
                                             ioc_parsing_rules=ioc_parsing_rules,
                                             include_source_ip=include_source_ip)
    if status:
        return OneTranslationCTIData(status=status, translations=translations, target_siem_type=platform.name)
    else:
        info_message = InfoMessage(message=translations, severity="error")
        return OneTranslationCTIData(info=info_message, status=status, target_siem_type=platform.name)
