import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from app.converter.core.mapping import DEFAULT_MAPPING_NAME
from app.converter.core.models.functions.types import ParsedFunctions


class MetaInfoContainer:
    def __init__(self, *,
                 id_: str = None,
                 title: str = None,
                 description: str = None,
                 author: str = None,
                 date: str = None,
                 license_: str = None,
                 severity: str = None,
                 references: List[str] = None,
                 tags: List[str] = None,
                 mitre_attack: List[str] = None,
                 status: str = None,
                 false_positives: List[str] = None,
                 source_mapping_ids: List[str] = None
                 ) -> None:
        self.id = id_ or str(uuid.uuid4())
        self.title = title or ""
        self.description = description or ""
        self.author = author or ""
        self.date = date or datetime.now().date().strftime("%Y-%m-%d")
        self.license = license_ or "DRL 1.1"
        self.severity = severity or "low"
        self.references = references or []
        self.tags = tags or []
        self.mitre_attack = mitre_attack or []
        self.status = status or "stable"
        self.false_positives = false_positives or []
        self.source_mapping_ids = source_mapping_ids or [DEFAULT_MAPPING_NAME]


@dataclass
class SiemContainer:
    query: list
    meta_info: MetaInfoContainer
    functions: ParsedFunctions = field(default_factory=ParsedFunctions)
