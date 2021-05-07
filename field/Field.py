

class Field:

    card = 0

    def __init__(self, card):
        self.card = card

    def operation(self,x1, x2, op):
        if op == "+":
            return self.sum(x1, x2)
        else:
            return self.prod(x1, x2)


    def sum(self, x1, x2):
        return (x1+x2) % self.card

    def prod(self, x1, x2):
        return (x1*x2) % self.card




