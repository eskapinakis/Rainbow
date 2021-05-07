from field import Field


class Rainbow:

    name = "rainbow"
    K = Field.Field(0)

    def __init__(self, order):
        self.K = Field.Field(order)

    def operation(self, x1, x2, op):
        return self.K.operation(x1, x2, op)