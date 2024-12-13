from typing import Optional

from fastapi import APIRouter, Body

from app.models.ioc_translation import CTIPlatform, OneTranslationCTIData
from app.models.translation import InfoMessage
from app.translator.cti_translator import cti_translator
from app.translator.tools.const import HashType, IocParsingRule, IOCType

iocs_router = APIRouter()


@iocs_router.post("/iocs/translate", description="Parse IOCs from text.")
@iocs_router.post("/iocs/translate", include_in_schema=False)
def parse_and_translate_iocs(
    text: str = Body(..., description="Text to parse IOCs from", embed=True),
    iocs_per_query: int = Body(25, description="IOCs per query limit", embed=True),
    platform: CTIPlatform = Body(..., description="Platform to parse IOCs to", embed=True),
    include_ioc_types: Optional[list[IOCType]] = Body(
        None, description="List of IOC types to include. By default all types are enabled.", embed=True
    ),
    include_hash_types: Optional[list[HashType]] = Body(
        None, description="List of hash types to include. By default all hash types are enabled.", embed=True
    ),
    exceptions: Optional[list[str]] = Body(
        None, description="List of exceptions. IOC is ignored if it contains one of exception values.", embed=True
    ),
    ioc_parsing_rules: Optional[list[IocParsingRule]] = Body(
        None, embed=True, description="Additional parsing parameters."
    ),
    include_source_ip: Optional[bool] = Body(False, description="Include source IP in query. By default it is false."),
) -> OneTranslationCTIData:
    status, translations = cti_translator.translate(
        text=text,
        platform_data=platform,
        iocs_per_query=iocs_per_query,
        include_ioc_types=include_ioc_types,
        include_hash_types=include_hash_types,
        exceptions=exceptions,
        ioc_parsing_rules=ioc_parsing_rules,
        include_source_ip=include_source_ip,
    )
    if status:
        return OneTranslationCTIData(status=status, translations=translations, target_platform_id=platform.id)

    info_message = InfoMessage(message=translations, severity="error")
    return OneTranslationCTIData(info=info_message, status=status, target_platform_id=platform.id)


@iocs_router.post("/iocs/generate", description="Parse IOCs from text and based on input data generate translation")
@iocs_router.post("/iocs/generate", include_in_schema=False)
def parse_iocs_and_generate_rule(
    text: str = Body(..., description="Text to parse IOCs from", embed=True),
    platform: CTIPlatform = Body(..., description="Platform to parse IOCs to", embed=True),
    iocs_per_query: int = Body(25, description="IOCs per query limit", embed=True),
    title: str = Body(..., description="Title", embed=True),
    description: str = Body(..., description="Description", embed=True),
    references: list[str] = Body(..., description="References", embed=True),
    created_date: str = Body(..., description="Rule created date", embed=True),
    mitre_tags: Optional[list[str]] = Body(..., description="Mitra tactics and techniques", embed=True),
) -> OneTranslationCTIData:
    status, translations = cti_translator.generate(
        title=title,
        text=text,
        platform_data=platform,
        description=description,
        references=references,
        created_date=created_date,
        mitre_tags=mitre_tags,
        iocs_per_query=iocs_per_query,
    )
    if status:
        return OneTranslationCTIData(status=status, translations=translations, target_platform_id=platform.id)

    info_message = InfoMessage(message=translations, severity="error")
    return OneTranslationCTIData(info=info_message, status=status, target_platform_id=platform.id)
