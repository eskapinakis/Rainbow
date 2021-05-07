class Field:

    order = 0
    isPrime = True

    def __init__(self, order):
        self.order = order

    def isPrime(self):
        for i in range(2, int(self.order**(1/2))+1):
            if self.order % i == 0:
                self.isPrime = False
                return

    def op(self, x1, x2, op):
        if self.isPrime:
            if op == "+":
                return self.sum(x1, x2)
            else:
                return self.prod(x1, x2)
        else:
            if op == "+":
                return self.weirdSum(x1, x2)
            else:
                return self.weirdProd(x1, x2)

    def sum(self, x1, x2):
        return (x1+x2) % self.order

    def prod(self, x1, x2):
        return (x1*x2) % self.order

    def weirdSum(self, x1, x2):
        return (x1+x2) % self.order

    def weirdProd(self, x1, x2):
        return (x1*x2) % self.order





