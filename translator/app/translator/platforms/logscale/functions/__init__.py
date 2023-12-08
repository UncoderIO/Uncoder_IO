import re

from app.translator.core.exceptions.functions import NotSupportedFunctionException, InvalidFunctionSignature
from app.translator.core.functions import PlatformFunctions
from app.translator.core.models.functions.base import ParsedFunctions
from app.translator.platforms.logscale.functions.const import LogScaleFunctionType
from app.translator.platforms.logscale.functions.manager import LogScaleFunctionsManager


class LogScaleFunctions(PlatformFunctions):
    manager = LogScaleFunctionsManager()

    def parse(self, query: str) -> tuple[ParsedFunctions, str]:
        parsed = []
        not_supported = []
        invalid = []
        functions = query.split(self.function_delimiter)
        query_part = ""
        for i, func in enumerate(functions):
            if not (func_name_match := re.search(r"(?P<func_name>[a-zA-Z:]+)\(", func)):
                if i == 0:
                    query_part = func
                    continue

                func = f"{LogScaleFunctionType.search}({func})"
                func_name_match = re.search(r"(?P<func_name>[a-zA-Z:]+)\(", func)
            func_name = func_name_match.group("func_name")
            func = func.strip()
            func_body = func[len(func_name)+1:len(func)-1]
            if func_parser := self.manager.get_parser(self.manager.get_generic_func_name(func_name)):
                try:
                    parsed.append(func_parser.parse(func_body))
                except NotSupportedFunctionException:
                    not_supported.append(func)
                except InvalidFunctionSignature:
                    invalid.append(func)
            else:
                not_supported.append(func)
        return ParsedFunctions(
            not_supported=[self.wrap_function_with_delimiter(func) for func in not_supported],
            functions=parsed,
            invalid=invalid
        ), query_part


log_scale_functions = LogScaleFunctions()
