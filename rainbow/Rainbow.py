from field import Field

class Rainbow:

    K = Field.Field(0)
    n = 0  # total number of variables
    u = 0  # partition size
    v = []  # numbers that create the partition
    S = []  # set S[i] of size v[i]
    o = []  # o[i] = v[i+1] - v[i] for i in 1,..,u-1
    O = []  # O[i] = S[i+1]\S[i] for i in 1,..,u-1

    alpha = []  # alpha[l][k][i][j] is the coefficient of oil-vinegar of layer l poly k
    beta = []  # alpha[l][k][i][j] is the coefficient of vinegar-vinegar of layer l poly k
    gamma = []  # gamma[l][k][i] is the linear term coefficient poly k
    eta = []  # eta[l][k] is the constant of each layer poly k

    L1 = []  # invertible matrix of n-v[1] x n - v[1]
    L2 = []  # n x n

    publicKey = 0
    privateKey = 0

    def __init__(self):
        self.K = Field.Field(29)

    def operation(self, x1, x2, op):
        return self.K.operation(x1, x2, op)

    def poly(self, l, k, x):
        return self.n

    def sign(self, m):
        return self.n

    def verify(self, m, sign):
        return self.n