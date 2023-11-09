from app.converter.core.models.functions.sort import SortOrderType, SortExpression


class AlaSortFunctionRender:

    sort_order_map = {SortOrderType.DESC: "desc", SortOrderType.ASC: "asc"}

    def __init__(self, function: SortExpression):
        self.function = function

    def render(self):
        result = "sort by "
        queries = []
        for field in self.function.fields:
            queries.append(f"{field.fieldname} {self.sort_order_map.get(field.order)}")
        result += ", ".join(queries)
        return result
