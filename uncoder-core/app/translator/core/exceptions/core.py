class NotImplementedException(BaseException):
    ...


class BasePlatformException(BaseException):
    ...


class StrictPlatformException(BasePlatformException):
    def __init__(self, platform_name: str, field_name: str):
        message = f"Platform {platform_name} has strict mapping. Source field {field_name} has no mapping."
        super().__init__(message)


class StrictPlatformFieldException(BasePlatformException):
    def __init__(self, platform_name: str, field_name: str):
        message = f"Source field `{field_name}` has no mapping for platform {platform_name}."
        super().__init__(message)


class UnsupportedPlatform(BasePlatformException):
    def __init__(self, platform: str, is_parser: bool = False):
        direction = "input" if is_parser else "output"
        if platform:
            message = (
                f"The selected {direction} language `{platform}` is not supported. "
                f"Please, select an option in the dropdown."
            )
        else:
            message = f"Please, select an {direction} language."
        super().__init__(message)


class UnsupportedRootAParser(BasePlatformException):
    def __init__(self, parser: str):
        message = (
            f"The platform `{parser}` specified in the body is not supported. "
            f"Please, use platform names listed in the readme.md"
        )
        super().__init__(message)


class RootAParserException(BasePlatformException):
    def __init__(self, platform_name: str, error: str):
        message = f"The body part of the detection section has invalid {platform_name} syntax. Error: {error}"
        super().__init__(message)


class YamlRuleValidationException(BasePlatformException):
    rule = None

    def __init__(self, missing_fields: list[str]):
        prepared_missing_fields = "\n".join(f"- {field}" for field in missing_fields)
        message = f"Invalid {self.rule} rule structure. Some required fields are missing: {prepared_missing_fields}."
        super().__init__(message)


class RootARuleValidationException(YamlRuleValidationException):
    rule = "RootA"


class SigmaRuleValidationException(YamlRuleValidationException):
    rule = "Sigma"


class InvalidRuleStructure(BasePlatformException):
    rule_type = None

    def __init__(self, error: str):
        message = f"Invalid {self.rule_type} structure. Issue: {error}."
        super().__init__(message)


class InvalidYamlStructure(InvalidRuleStructure):
    rule_type: str = "YAML"


class InvalidJSONStructure(InvalidRuleStructure):
    rule_type: str = "JSON"


class InvalidXMLStructure(InvalidRuleStructure):
    rule_type: str = "XML"
