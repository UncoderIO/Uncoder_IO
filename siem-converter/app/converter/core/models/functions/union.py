class UnionExpression:
    def __init__(self, fieldname: str, fields: list = []):
        self.fieldname = fieldname
        self.fields = fields