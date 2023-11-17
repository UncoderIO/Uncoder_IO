from typing import List

from app.converter.core.functions import Functions, ParsedFunctions, NotSupportedFunction
import re


class LogScaleQueryFunctions(Functions):
    siem_type = 'humio'
    functions_classes = []

    def prepare_not_supported(self, not_supported: List[NotSupportedFunction]) -> list:
        for n in range(len(not_supported)):
            not_supported[n] = f'| {not_supported[n].query}'
        return not_supported

    def parse(self, query: str) -> ParsedFunctions:
        result = []
        not_supported = []
        functions = query.split(self.function_delimiter)
        query_result = []
        for i in range(len(functions)):
            if func_match := re.search('(\w+)\(([^)]+)\)', functions[i]):
                func_name = func_match.group().split('(')[0]
                for func in functions[i:]:
                    not_supported.append(NotSupportedFunction(name=func_name, query=func))
                return ParsedFunctions(not_supported=self.prepare_not_supported(not_supported), functions=result), query_result
            else:
                query_result.append(functions[i])
        return ParsedFunctions(not_supported=self.prepare_not_supported(not_supported), functions=result), query_result