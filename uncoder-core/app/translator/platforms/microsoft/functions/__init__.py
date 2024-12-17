import os.path

from app.translator.core.exceptions.functions import InvalidFunctionSignature, NotSupportedFunctionException
from app.translator.core.functions import PlatformFunctions
from app.translator.core.models.functions.base import ParsedFunctions
from app.translator.platforms.microsoft.functions.const import KQLFunctionType
from app.translator.platforms.microsoft.functions.manager import (
    MicrosoftFunctionsManager,
    microsoft_defender_functions_manager,
    microsoft_sentinel_functions_manager,
)


class MicrosoftFunctions(PlatformFunctions):
    dir_path: str = os.path.abspath(os.path.dirname(__file__))

    def parse(self, query: str) -> tuple[str, str, ParsedFunctions]:
        parsed = []
        not_supported = []
        invalid = []
        split_query = query.split(self.function_delimiter)
        table = split_query[0].strip()
        query_parts = []
        for func in split_query[1:]:
            func = func.strip()
            split_func = func.split(" ")
            func_name, func_body = split_func[0], " ".join(split_func[1:])
            if func_name == KQLFunctionType.where:
                query_parts.append(func_body)
                continue

            try:
                func_parser = self.manager.get_hof_parser(func_name)
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


class MicrosoftSentinelFunctions(MicrosoftFunctions):
    manager: MicrosoftFunctionsManager = microsoft_sentinel_functions_manager


class MicrosoftDefenderFunctions(MicrosoftFunctions):
    manager: MicrosoftFunctionsManager = microsoft_defender_functions_manager


microsoft_sentinel_functions = MicrosoftSentinelFunctions()
microsoft_defender_functions = MicrosoftDefenderFunctions()
