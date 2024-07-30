import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional

from app.translator.core.const import QUERY_TOKEN_TYPE
from app.translator.core.custom_types.meta_info import SeverityType
from app.translator.core.mapping import DEFAULT_MAPPING_NAME
from app.translator.core.models.functions.base import ParsedFunctions
from app.translator.core.models.query_tokens.field import Field


@dataclass
class MitreTechniqueContainer:
    technique_id: str
    name: str
    url: str
    tactic: list[str]


@dataclass
class MitreTacticContainer:
    external_id: str
    url: str
    name: str


@dataclass
class MitreInfoContainer:
    tactics: list[MitreTacticContainer] = field(default_factory=list)
    techniques: list[MitreTechniqueContainer] = field(default_factory=list)


class MetaInfoContainer:
    def __init__(
        self,
        *,
        id_: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        author: Optional[list[str]] = None,
        date: Optional[str] = None,
        output_table_fields: Optional[list[Field]] = None,
        query_fields: Optional[list[Field]] = None,
        license_: Optional[str] = None,
        severity: Optional[str] = None,
        references: Optional[list[str]] = None,
        tags: Optional[list[str]] = None,
        raw_mitre_attack: Optional[list[str]] = None,
        status: Optional[str] = None,
        false_positives: Optional[list[str]] = None,
        source_mapping_ids: Optional[list[str]] = None,
        parsed_logsources: Optional[dict] = None,
        timeframe: Optional[timedelta] = None,
        mitre_attack: MitreInfoContainer = MitreInfoContainer(),
    ) -> None:
        self.id = id_ or str(uuid.uuid4())
        self.title = title or ""
        self.description = description or ""
        self.author = [v.strip() for v in author] if author else []
        self.date = date or datetime.now().date().strftime("%Y-%m-%d")
        self.output_table_fields = output_table_fields or []
        self.query_fields = query_fields or []
        self.license = license_ or "DRL 1.1"
        self.severity = severity or SeverityType.low
        self.references = references or []
        self.tags = tags or []
        self.mitre_attack = mitre_attack or None
        self.raw_mitre_attack = raw_mitre_attack or []
        self.status = status or "stable"
        self.false_positives = false_positives or []
        self.source_mapping_ids = sorted(source_mapping_ids) if source_mapping_ids else [DEFAULT_MAPPING_NAME]
        self.parsed_logsources = parsed_logsources or {}
        self.timeframe = timeframe

    @property
    def author_str(self) -> str:
        return ", ".join(self.author)


@dataclass
class RawQueryContainer:
    query: str
    language: str
    meta_info: MetaInfoContainer = field(default_factory=MetaInfoContainer)


@dataclass
class RawQueryDictContainer:
    query: dict
    language: str
    meta_info: dict


@dataclass
class TokenizedQueryContainer:
    tokens: list[QUERY_TOKEN_TYPE]
    meta_info: MetaInfoContainer
    functions: ParsedFunctions = field(default_factory=ParsedFunctions)
