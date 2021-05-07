

class Field:

    order = 0

    def __init__(self, order):
        self.order = order

    def operation(self, x1, x2, op):
        if op == "+":
            return self.sum(x1, x2)
        else:
            return self.prod(x1, x2)

    def sum(self, x1, x2):
        return (x1+x2) % self.order

    def prod(self, x1, x2):
        return (x1*x2) % self.order




