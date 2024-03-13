from typing import Optional

from pydantic import BaseModel

from app.models.translation import InfoMessage


class CTIPlatform(BaseModel):
    id: str


class OneTranslationCTIData(BaseModel):
    info: Optional[InfoMessage] = None
    status: bool
    translations: Optional[list] = None
    target_platform_id: str
