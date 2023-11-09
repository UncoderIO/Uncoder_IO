from dataclasses import dataclass
from typing import Optional


@dataclass
class PlatformDetails:
    siem_type: str = ""
    name: str = ""
    platform_name: str = ""
    group_id: Optional[str] = None
    group_name: Optional[str] = None
    alt_platform_name: Optional[str] = "Default"
    alt_platform: Optional[str] = "regular"
    first_choice: Optional[int] = 1
