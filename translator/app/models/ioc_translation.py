from typing import Optional

from pydantic import BaseModel

from app.models.translation import InfoMessage


class CTIPlatform(BaseModel):
    name: str


class OneTranslationCTIData(BaseModel):
    info: Optional[InfoMessage] = None
    status: bool
    translations: Optional[list] = None
    target_siem_type: str
