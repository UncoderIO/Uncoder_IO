from app.translator.core.exceptions.functions import InvalidFunctionSignature, NotSupportedFunctionException
from app.translator.core.functions import PlatformFunctions
from app.translator.core.models.functions.base import ParsedFunctions
from app.translator.platforms.microsoft.functions.const import KQLFunctionType
from app.translator.platforms.microsoft.functions.manager import MicrosoftFunctionsManager


class MicrosoftFunctions(PlatformFunctions):
    def __init__(self):
        self.manager = MicrosoftFunctionsManager()

    def parse(self, query: str) -> tuple[str, str, ParsedFunctions]:
        parsed = []
        not_supported = []
        invalid = []
        split_query = query.split(self.function_delimiter)
        table = split_query[0].strip()
        query_parts = []
        for func in split_query[1:]:
            split_func = func.strip(" ").split(" ")
            func_name, func_body = split_func[0], " ".join(split_func[1:])
            if func_name == KQLFunctionType.where:
                query_parts.append(func_body)
                continue

            try:
                func_parser = self.manager.get_parser(self.manager.get_generic_func_name(func_name))
                parsed.append(func_parser.parse(func_body, func))
            except NotSupportedFunctionException:
                not_supported.append(func)
            except InvalidFunctionSignature:
                invalid.append(func)
        result_query = " and ".join(f"({query_part})" for query_part in query_parts)
        return (
            table,
            result_query,
            ParsedFunctions(
                functions=parsed,
                not_supported=[self.wrap_function_with_delimiter(func) for func in not_supported],
                invalid=invalid,
            ),
        )


microsoft_sentinel_functions = MicrosoftFunctions()
microsoft_defender_functions = MicrosoftFunctions()
