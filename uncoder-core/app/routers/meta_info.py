from dataclasses import asdict

from fastapi import APIRouter, Body, HTTPException

from app.models.meta_info import (
    MetaInfo,
    MetaInfoResponse,
    MitreInfoContainer,
    MitreTacticContainer,
    MitreTechniqueContainer,
    ParsedLogSources,
    RawMetaInfo,
)
from app.translator.core.exceptions.core import UnsupportedPlatform
from app.translator.translator import app_translator

meta_info_router = APIRouter()


@meta_info_router.post("/get_meta_info/", tags=["meta_info"], description="Get Rule MetaInfo")
@meta_info_router.post("/get_meta_info/", include_in_schema=False)
def get_meta_info_data(
    source_platform_id: str = Body(..., embed=True), text: str = Body(..., embed=True)
) -> MetaInfoResponse:
    try:
        logsources, raw_query_container = app_translator.parse_meta_info(text=text, source=source_platform_id)
    except UnsupportedPlatform as exc:
        raise HTTPException(status_code=400, detail="Unsuported platform") from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Unexpected error.") from exc
    if not raw_query_container:
        raise HTTPException(status_code=400, detail="Can't parse metadata")
    most_frequent_product = max(logsources.get("product"), key=logsources.get("product").get, default=None)
    most_frequent_service = max(logsources.get("service"), key=logsources.get("service").get, default=None)
    most_frequent_category = max(logsources.get("category"), key=logsources.get("category").get, default=None)

    logsources.get("product", {}).pop(most_frequent_product, None)
    logsources.get("service", {}).pop(most_frequent_service, None)
    logsources.get("category", {}).pop(most_frequent_category, None)

    parsed_logsources = ParsedLogSources(
        most_frequent_product=most_frequent_product,
        most_frequent_service=most_frequent_service,
        most_frequent_category=most_frequent_category,
        least_frequent_products=list(logsources.get("product", {}).keys()),
        least_frequent_services=list(logsources.get("service", {}).keys()),
        least_frequent_categories=list(logsources.get("category", {}).keys()),
    )
    return MetaInfoResponse(
        query=raw_query_container.query,
        language=raw_query_container.language,
        meta_info=MetaInfo(
            id_=raw_query_container.meta_info.id,
            title=raw_query_container.meta_info.title,
            description=raw_query_container.meta_info.description,
            author=raw_query_container.meta_info.author,
            date=raw_query_container.meta_info.date,
            false_positives=raw_query_container.meta_info.false_positives,
            license_=raw_query_container.meta_info.license,
            mitre_attack=MitreInfoContainer(
                tactics=[
                    MitreTacticContainer(**asdict(tactic_container))
                    for tactic_container in raw_query_container.meta_info.mitre_attack.tactics
                ],
                techniques=[
                    MitreTechniqueContainer(**asdict(tactic_container))
                    for tactic_container in raw_query_container.meta_info.mitre_attack.techniques
                ],
            ),
            output_table_fields=raw_query_container.meta_info.output_table_fields,
            parsed_log_sources=parsed_logsources,
            query_fields=raw_query_container.meta_info.query_fields + raw_query_container.meta_info.function_fields,
            query_period=raw_query_container.meta_info.query_period,
            raw_metainfo_container=RawMetaInfo(
                trigger_operator=raw_query_container.meta_info.raw_metainfo_container.trigger_operator,
                trigger_threshold=raw_query_container.meta_info.raw_metainfo_container.trigger_threshold,
                query_frequency=raw_query_container.meta_info.raw_metainfo_container.query_frequency,
                query_period=raw_query_container.meta_info.raw_metainfo_container.query_period,
            ),
            raw_mitre_attack=raw_query_container.meta_info.raw_mitre_attack,
            references=raw_query_container.meta_info.references,
            severity=raw_query_container.meta_info.severity,
            source_mapping_ids=raw_query_container.meta_info.source_mapping_ids,
            status=raw_query_container.meta_info.status,
            tags=raw_query_container.meta_info.tags,
            timeframe=raw_query_container.meta_info.timeframe,
        ),
    )
