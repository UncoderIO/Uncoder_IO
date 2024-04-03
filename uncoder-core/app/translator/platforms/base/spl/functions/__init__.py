import re

from app.translator.core.exceptions.functions import InvalidFunctionSignature, NotSupportedFunctionException
from app.translator.core.functions import PlatformFunctions
from app.translator.core.models.functions.base import ParsedFunctions
from app.translator.core.models.query_container import RawQueryContainer, TokenizedQueryContainer
from app.translator.platforms.base.spl.functions.const import SplFunctionType
from app.translator.platforms.base.spl.functions.manager import SplFunctionsManager


class SplFunctions(PlatformFunctions):
    manager = SplFunctionsManager()

    @staticmethod
    def prepare_query(query: str) -> str:
        if query.startswith(SplFunctionType.search):
            query = re.sub(SplFunctionType.search, "", query, 1)
        return query

    def parse(self, query: str) -> tuple[str, ParsedFunctions]:
        parsed = []
        not_supported = []
        invalid = []
        functions = query.split(self.function_delimiter)
        result_query = self.prepare_query(functions[0])
        for func in functions[1:]:
            split_func = func.strip().split(" ")
            func_name, func_body = split_func[0], " ".join(split_func[1:])
            try:
                func_parser = self.manager.get_parser(self.manager.get_generic_func_name(func_name))
                parsed.append(func_parser.parse(func_body, func))
            except NotSupportedFunctionException:
                not_supported.append(func)
            except InvalidFunctionSignature:
                invalid.append(func)

        return result_query, ParsedFunctions(
            functions=parsed,
            not_supported=[self.wrap_function_with_delimiter(func) for func in not_supported],
            invalid=invalid,
        )

    @staticmethod
    def parse_tstats_func(raw_query_container: RawQueryContainer) -> TokenizedQueryContainer:
        raise NotSupportedFunctionException
