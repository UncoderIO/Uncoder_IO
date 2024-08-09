from app.translator.const import DEFAULT_VALUE_TYPE
from app.translator.core.escape_manager import EscapeManager
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.render import BaseFieldValueRender, PlatformQueryRender
from app.translator.managers import render_manager
from app.translator.platforms.carbonblack.const import carbonblack_query_details
from app.translator.platforms.carbonblack.escape_manager import carbon_black_escape_manager
from app.translator.platforms.carbonblack.mapping import CarbonBlackMappings, carbonblack_query_mappings


class CarbonBlackFieldValueRender(BaseFieldValueRender):
    details: PlatformDetails = carbonblack_query_details
    escape_manager: EscapeManager = carbon_black_escape_manager

    def equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.equal_modifier(field=field, value=v) for v in value)})"
        return f'{field}:"{self.apply_value(value)}"'

    def not_equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            values = [self.apply_value(val) for val in value]
            return f"(NOT {field}:({self.or_token.join(values)})"
        return f"(NOT {field}:{self.apply_value(value)})"

    def contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            values = [f"*{self.apply_value(val)}*" for val in value]
            return f"{field}:({self.or_token.join(values)})"
        return f"{field}:*{self.apply_value(value)}*"

    def endswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            values = [f"*{self.apply_value(val)}" for val in value]
            return f"{field}:({self.or_token.join(values)})"
        return f"{field}:*{self.apply_value(value)}"

    def startswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            values = [f"{self.apply_value(val)}*" for val in value]
            return f"{field}:({self.or_token.join(values)})"
        return f"{field}:{self.apply_value(value)}*"

    def regex_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.regex_modifier(field=field, value=v) for v in value)})"
        return f"{field}:/{value}/"

    def keywords(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.keywords(field=field, value=v) for v in value)})"
        return f"(*{value}*)"

    def is_none(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.is_none(field=field, value=v) for v in value)})"
        return f"NOT _exists_:{field}"

    def is_not_none(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.is_not_none(field=field, value=v) for v in value)})"
        return f"_exists_:{field}"


@render_manager.register
class CarbonBlackQueryRender(PlatformQueryRender):
    details: PlatformDetails = carbonblack_query_details
    mappings: CarbonBlackMappings = carbonblack_query_mappings

    or_token = "OR"
    and_token = "AND"
    not_token = "NOT"

    comment_symbol = "//"

    field_value_render = CarbonBlackFieldValueRender(or_token=or_token)
