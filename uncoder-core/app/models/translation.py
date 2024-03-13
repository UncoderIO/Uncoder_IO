from typing import Optional

from pydantic import BaseModel


class InfoMessage(BaseModel):
    message: str
    severity: str


class OneTranslationData(BaseModel):
    info: Optional[InfoMessage] = None
    status: bool
    translation: Optional[str] = None
    target_platform_id: str


class TranslatorPlatform(BaseModel):
    name: str
    id: str
    code: str
    group_name: str
    group_id: str
    platform_name: str
    platform_id: str
    alt_platform_name: str = "Default"
    alt_platform: str = "regular"
    first_choice: int = 1


class TranslatorPlatforms(BaseModel):
    renders: list
    parsers: list


class Platform(BaseModel):
    id: str
    name: str
    code: str
    group_name: str
    group_id: str
    renders: Optional[list]
    parsers: Optional[list]
