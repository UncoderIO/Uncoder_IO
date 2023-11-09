from app.converter.core.models.functions.types import ParsedFunctions, NotSupportedFunction


class Functions:
    siem_type: str
    parser_functions_map = {}
    function_delimiter = "|"

    def parse(self, query: str) -> ParsedFunctions:
        result = []
        not_supported = []
        functions = query.split(self.function_delimiter)
        for function in functions:
            function_name = function.split(' ')[0]
            if function_name in self.parser_functions_map:
                pass
            else:
                not_supported.append(NotSupportedFunction(name=function_name, query=function))
        return ParsedFunctions(not_supported=self.prepare_not_supported(not_supported), functions=result)

    def prepare_not_supported(self, not_supported):
        for n in range(len(not_supported)):
            not_supported[n] = f'| {not_supported[n].query}'
        return not_supported
