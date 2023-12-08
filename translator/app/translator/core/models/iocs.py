from dataclasses import dataclass


@dataclass
class IocsChunkValue:
    generic_field: str
    platform_field: str
    value: str
