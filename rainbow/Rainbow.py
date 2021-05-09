# from field import Field
import random as rand
from pyfinite import ffield as ff  # k=ff.FField(8)
from pyfinite import genericmatrix as gm


class Rainbow:
    K = ff.FField(8)
    order = 0
    n = 0  # total number of variables
    u = 0  # partition size
    v = []  # numbers that create the partition
    S = []  # set S[i] of size v[i]
    o = []  # o[i] = v[i+1] - v[i] for i in 1,..,u-1
    O = []  # O[i] = S[i+1]\S[i] for i in 1,..,u-1

    alpha = []  # alpha[l][k][i][j] is the coefficient of oil-vinegar of layer l poly k
    beta = []  # beta[l][k][i][j] is the coefficient of vinegar-vinegar of layer l poly k
    gamma = []  # gamma[l][k][i] is the linear term coefficient poly k
    eta = []  # eta[l][k] is the constant of each layer poly k

    L1 = []  # invertible matrix of n-v[1] x n - v[1]
    L2 = []  # n x n

    publicKey = 0
    privateKey = 0

    def __init__(self):
        self.K = ff.FField(8)  # K.sum(x1,x2)
        self.order = 2 ** 8
        self.n = 33
        self.u = 5
        self.v = [6, 12, 17, 22, 33]
        self.o = [6, 5, 5, 11]
        self.S = [[i for i in range(v)] for v in self.v]
        self.O = [[j for j in range(self.v[i], self.v[i + 1])] for i in range(len(self.v) - 1)]

        # u-1 e o numero de camadas
        # o[l] e o numero de polys
        # os outros sao o numero de variaveis oil ou vinegar
        self.alpha = [[[[rand.randint(0, self.order - 1) for _ in self.O[l]] for _ in self.S[l]] for
                       _ in range(self.o[l])] for l in range(self.u - 1)]

        self.beta = [[[[rand.randint(0, self.order - 1) for _ in self.S[l]] for _ in self.S[l]] for
                      _ in range(self.o[l])] for l in range(self.u - 1)]

        self.gamma = [[[rand.randint(0, self.order - 1) for _ in self.S[l+1]] for _ in range(self.o[l])]
                      for l in range(self.u-1)]

        self.eta = [[rand.randint(0, self.order - 1) for _ in range(self.o[l])] for l in range(self.u-1)]

        self.L1 = self.invertibleMatrix(self.n-self.v[1])
        self.L2 = self.invertibleMatrix(self.n)

        for i in self.L1:
            print(i)

        #m1 = [[1,4,6],[0,1,3],[0,0,1]]
        #m2 = [[1,0,0],[8,1,0],[13,2,1]]
        #for i in self.matrixProd(3, m1, m2):
        #    print(i)

    def invertibleMatrix(self,n):
        matrix1 = [[0 for _ in range(n)] for _ in range(n)]
        matrix2 = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i):
                matrix1[i][j] = rand.randint(0, self.order-1)
                matrix2[n-i-1][n-j-1] = rand.randint(0, self.order - 1)
        for i in range(n):
            matrix1[i][i] = 1
            matrix2[i][i] = 1
        return self.matrixProd(n, matrix1, matrix2)

    def matrixProd(self, n, m1, m2):
        matrix = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                entry = 0
                for k in range(n):
                    entry = self.K.Add(entry, self.K.Multiply(m1[k][i], m2[j][k]))
                    #entry += m1[k][i]*m2[j][k]
                matrix[i][j] = entry
        return matrix



    # l is the layer
    # k is the index of the poly
    # x is the variables
    def poly(self, l, k, x):
        eval = self.eta[l][k]
        eval = self.K.Add(eval, self.oilVin(l, k, x))
        eval = self.K.Add(eval, self.vinVin(l, k, x))
        eval = self.K.Add(eval, self.linear(l, k, x))
        return eval

    def oilVin(self, l, k, x):
        eval = 0
        for i in range(self.o[l]):
            for j in self.S[l]:
                var = self.K.Multiply(x[i], x[j])
                eval = self.K.Add(eval, self.K.Multiply(self.alpha[l][k][j][i], var))
        return eval

    def vinVin(self, l, k, x):
        eval = 0
        for i in self.S[l]:
            for j in self.S[l]:
                var = self.K.Multiply(x[i], x[j])
                eval = self.K.Add(eval, self.K.Multiply(self.beta[l][k][i][j], var))
        return eval

    def linear(self, l, k, x):
        eval = 0
        for i in self.S[l+1]:
            eval = self.K.Add(eval, self.K.Multiply(self.gamma[l][k][i], x[i]))
        return eval

    def op(self, x1, x2, op):
        return self.K.op(x1, x2, op)

    # x should be an array x1,...,xn
    # F goes from K^n to K^{n-v1}
    def F(self, x):
        m = self.n - self.v[0]
        result = [0] * m  # (0,...,0)
        for l in range(self.u-1):
            for k in range(self.o[l]):
                result[self.index(l, k)] = self.poly(l, k, x)
        return result

    def index(self, l, k):
        return (self.v[l]-self.v[0])+k

    def sign(self, m):
        return self.n

    def verify(self, m, sign):
        return self.n
