from app.converter.core.functions import Functions
from app.converter.core.models.functions.types import ParsedFunctions, NotSupportedFunction


class MicroSoftQueryFunctions(Functions):

    def parse(self, query: str):
        result = []
        functions = query.split(self.function_delimiter)
        query_result = [functions.pop(0).strip()]
        not_supported = []
        for function in functions:
            function_name = function.strip(" ").split(' ')[0]
            if function_name.lower() == "where":
                query_result.append(f'({function.lstrip("where ")})')
            elif function_name in self.parser_functions_map:
                pass
            else:
                not_supported.append(NotSupportedFunction(name=function_name, query=function))
        return ParsedFunctions(not_supported=self.prepare_not_supported(not_supported), functions=result), query_result
