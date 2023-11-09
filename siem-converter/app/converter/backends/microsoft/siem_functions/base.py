from app.converter.backends.microsoft.siem_functions.aggregation import AlaAggregationFunctionRender
from app.converter.backends.microsoft.siem_functions.search import AlaSearchFunctionRender
from app.converter.backends.microsoft.siem_functions.sort import AlaSortFunctionRender
from app.converter.backends.microsoft.siem_functions.table import AlaTableFunctionRender
from app.converter.core.functions import Functions
from app.converter.core.models.functions.aggregation import AggregationExpression
from app.converter.core.models.functions.search import SearchExpression
from app.converter.core.models.functions.sort import SortExpression
from app.converter.core.models.functions.table import TableExpression
from app.converter.core.models.functions.types import ParsedFunctions, NotSupportedFunction


class MicroSoftQueryFunctions(Functions):

    render_functions_map = {
        SortExpression: AlaSortFunctionRender, 
        SearchExpression: AlaSearchFunctionRender,
        AggregationExpression: AlaAggregationFunctionRender,
        TableExpression: AlaTableFunctionRender,
        # WhereExpression: AlaWhereFunctionRender
    }

    def render(self, functions: list):
        query = "| "
        funcs = []
        for function in functions:
            if render_class := self.render_functions_map.get(type(function)):
                funcs.append(render_class(function).render())
        query += " | ".join(funcs)
        query = query.rstrip(" ")
        return query

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
