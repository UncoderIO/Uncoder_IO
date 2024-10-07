from typing import Optional

from pydantic import BaseModel, Field


class ParsedLogSources(BaseModel):
    most_frequent_product: Optional[str]
    most_frequent_service: Optional[str]
    most_frequent_category: Optional[str]
    least_frequent_products: Optional[list[str]] = Field(default_factory=list)
    least_frequent_services: Optional[list[str]] = Field(default_factory=list)
    least_frequent_categories: Optional[list[str]] = Field(default_factory=list)


class MitreTechniqueContainer(BaseModel):
    technique_id: Optional[str]
    name: Optional[str]
    url: Optional[str]
    tactic: Optional[list[str]]


class MitreTacticContainer(BaseModel):
    external_id: Optional[str]
    url: Optional[str]
    name: Optional[str]


class MitreInfoContainer(BaseModel):
    tactics: Optional[list[MitreTacticContainer]] = Field(default_factory=list)
    techniques: Optional[list[MitreTechniqueContainer]] = Field(default_factory=list)


class RawMetaInfo(BaseModel):
    trigger_operator: Optional[str] = Field(default_factory=str)
    trigger_threshold: Optional[str] = Field(default_factory=str)
    query_frequency: Optional[str] = Field(default_factory=str)
    query_period: Optional[str] = Field(default_factory=str)


class MetaInfo(BaseModel):
    id_: str = Field(default_factory=str)
    title: Optional[str] = Field(default_factory=str)
    description: Optional[str] = Field(default_factory=str)
    author: Optional[list] = Field(default_factory=list)
    date: Optional[str] = Field(default_factory=str)
    false_positives: Optional[list] = Field(default_factory=list)
    license_: Optional[str] = Field(default_factory=str)
    mitre_attack: Optional[MitreInfoContainer] = Field(default_factory=list)
    output_table_fields: Optional[list] = Field(default_factory=list)
    parsed_log_sources: Optional[ParsedLogSources] = Field(default_factory=ParsedLogSources)
    query_fields: Optional[list] = Field(default_factory=list)
    query_period: Optional[str] = Field(default_factory=str)
    raw_meta_info_container: Optional[RawMetaInfo] = Field(default_factory=RawMetaInfo)
    raw_mitre_attack: Optional[list] = Field(default_factory=list)
    references: Optional[list] = Field(default_factory=list)
    severity: Optional[str] = Field(default_factory=str)
    source_mapping_ids: Optional[list] = Field(default_factory=list)
    status: Optional[str] = Field(default_factory=str)
    tags: Optional[list] = Field(default_factory=list)
    timeframe: Optional[str] = Field(default_factory=str)


class MetaInfoResponse(BaseModel):
    query: str
    language: str
    meta_info: Optional[MetaInfo] = Field(default_factory=MetaInfo)
