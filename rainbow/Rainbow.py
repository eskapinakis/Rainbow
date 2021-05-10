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

    def __init__(self, power, message_size, partition_size):

        # create a field of size 2^power
        self.K = ff.FField(power)
        self.order = 2 ** power

        # creates a random partition for the message space
        self.n = message_size  # the message size is actually n - v[0] = n-1 cause I can
        self.u = partition_size  # u-1 vai ser o numero de camadas arco-iris
        m = int(message_size/(partition_size - 1))
        self.v = [0]*partition_size
        self.v[0] = 1  # rand.randint(1, m)
        for i in range(1, self.u-1):
            self.v[i] = rand.randint(self.v[i-1]+1, m*(i+1)-1)
        self.v[partition_size-1] = self.n  # the last element has to equal the message size
        # print(self.v)

        self.o = [self.v[l] - self.v[l - 1] for l in range(1, self.u)]  # numero de polinomios
        self.S = [[i for i in range(v)] for v in self.v]  # variaveis vinegar
        self.O = [[j for j in range(self.v[i], self.v[i + 1])] for i in range(len(self.v) - 1)]  # vairaveis oil

        self.alpha = [[[[rand.randint(0, self.order - 1) for _ in self.O[l]] for _ in self.S[l]] for
                       _ in range(self.o[l])] for l in range(self.u - 1)]

        self.beta = [[[[rand.randint(0, self.order - 1) for _ in self.S[l]] for _ in self.S[l]] for
                      _ in range(self.o[l])] for l in range(self.u - 1)]

        self.gamma = [[[rand.randint(0, self.order - 1) for _ in self.S[l + 1]] for _ in range(self.o[l])]
                      for l in range(self.u - 1)]

        self.eta = [[rand.randint(0, self.order - 1) for _ in range(self.o[l])] for l in range(self.u - 1)]

        self.L1 = self.invertibleMatrix(self.n - self.v[0])
        self.L2 = self.invertibleMatrix(self.n)

    # matrix multiplied by a vector
    def matrixVectorProd(self, m1, m2):
        n = len(m1)
        m = len(m2)
        matrix = [0 for _ in range(n)]
        for i in range(n):
            entry = 0
            for j in range(m):
                entry = self.K.Add(entry, self.K.Multiply(m1[i][j], m2[j]))
                # entry += m1[i][j]*m2[j]
            matrix[i] = entry
        return matrix

    # product of two matrices
    def matrixProd(self, m1, m2):
        n = len(m1)
        m = len(m2[0])
        N = len(m2)
        matrix = [[0 for _ in range(n)] for _ in range(m)]
        for i in range(n):
            for j in range(m):
                entry = 0
                for k in range(N):
                    entry = self.K.Add(entry, self.K.Multiply(m1[i][k], m2[k][j]))
                    # entry += m1[i][k]*m2[k][j]
                matrix[i][j] = entry
        return matrix

    # Creates an invertible matrix of size n
    def invertibleMatrix(self, n):
        matrix1 = [[0 for _ in range(n)] for _ in range(n)]
        matrix2 = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i):
                matrix1[i][j] = rand.randint(0, self.order - 1)
                matrix2[n - i - 1][n - j - 1] = rand.randint(0, self.order - 1)
        for i in range(n):
            matrix1[i][i] = rand.randint(1, self.order - 1)
            matrix2[i][i] = rand.randint(1, self.order - 1)

        SUM = lambda x, y: self.K.Add(x, y)
        SUB = lambda x, y: self.K.Subtract(x, y)
        PROD = lambda x, y: self.K.Multiply(x, y)
        DIV = lambda x, y: self.K.Divide(x, y)

        m1 = gm.GenericMatrix(size=(n, n), zeroElement=0, identityElement=1, add=SUM, mul=PROD, sub=SUB, div=DIV)
        for i in range(n):
            m1.SetRow(i, matrix1[i])
        m2 = gm.GenericMatrix(size=(n, n), zeroElement=0, identityElement=1, add=SUM, mul=PROD, sub=SUB, div=DIV)
        for i in range(n):
            m2.SetRow(i, matrix2[i])

        return m1 * m2

    # l is the layer
    # k is the index of the poly
    # x is the variables
    def poly(self, l, k, x):
        eval = self.eta[l][k]
        eval = self.K.Add(eval, self.oilVin(l, k, x))
        eval = self.K.Add(eval, self.vinVin(l, k, x))
        eval = self.K.Add(eval, self.linear(l, k, x))
        return eval

    # sum of oil-vinegar coefficients
    def oilVin(self, l, k, x):
        eval = 0
        for i in range(self.o[l]):
            for j in self.S[l]:
                I = self.O[l][i]
                var = self.K.Multiply(x[I], x[j])
                eval = self.K.Add(eval, self.K.Multiply(self.alpha[l][k][j][i], var))
        return eval

    # sum of vinegar-vinegar coefficients
    def vinVin(self, l, k, x):
        eval = 0
        for i in self.S[l]:
            for j in self.S[l]:
                var = self.K.Multiply(x[i], x[j])
                eval = self.K.Add(eval, self.K.Multiply(self.beta[l][k][i][j], var))
        return eval

    # sum of linear coefficients
    def linear(self, l, k, x):
        eval = 0
        for i in self.S[l + 1]:
            eval = self.K.Add(eval, self.K.Multiply(self.gamma[l][k][i], x[i]))
        return eval

    # x should be an array x1,...,xn
    # F goes from K^n to K^{n-v1}
    def F(self, x):
        m = self.n - self.v[0]
        result = [0] * m  # (0,...,0)
        for l in range(self.u - 1):
            for k in range(self.o[l]):
                result[self.index(l, k)] = self.poly(l, k, x)
        return result

    def FTilde(self, x):
        L2 = self.makeArrayFromMatrix(self.L2)
        L1 = self.makeArrayFromMatrix(self.L1)
        x = self.matrixVectorProd(L2, x)
        x = self.F(x)
        x = self.matrixVectorProd(L1, x)
        return x  # L1 o F o L2(x)

    def findSolution(self, y):
        L2_inv = self.makeArrayFromMatrix(self.L2.Inverse())
        L1_inv = self.makeArrayFromMatrix(self.L1.Inverse())
        y = self.matrixVectorProd(L1_inv, y)

        x = [0] * self.n  # this is the part of the solution that we guess
        for i in range(self.v[0]):
            x[i] = rand.randint(0, self.order - 1)

        # Cada passo do sistema
        for l in range(self.u - 1):
            # l = 0
            # Queremos resolver A[x] = [b]
            # Criar novo [b]
            Y = y[self.v[l] - self.v[0]: self.v[l + 1] - self.v[0]]
            # k percorre os índices todos da subcamada
            for k in range(self.o[l]):
                # i = self.index(l,k) # identifica o índice em Y dada a camada e subcamada
                Y[k] = self.K.Subtract(Y[k], self.eta[l][k])
                Y[k] = self.K.Subtract(Y[k], self.vinVin(l, k, x[0:self.v[l]]))  # S[l] = {1,..,v[l]}

                temp = 0
                for p in self.S[l]:
                    temp = self.K.Add(temp, self.K.Multiply(self.gamma[l][k][p], x[p]))

                Y[k] = self.K.Subtract(Y[k], temp)  # S[l+1] = S[l] U O[l]
                # for k in range(self.o[ltemp]):
                #     i = self.index(ltemp,k) # identifica o índice em Y dada a camada e subcamada

                #     Y[i] = self.K.Subtract(Y[i], self.eta[ltemp][k])
                #     Y[i] = self.K.Subtract(Y[i], self.vinVin(ltemp, k, x[0:self.v[ltemp]])) # S[l] = {1,..,v[l]}
                #     Y[i] = self.K.Subtract(Y[i], self.linear(ltemp-1, k, x[0:self.v[ltemp]])) # S[l+1] = S[l] U O[l]

            # Criar A
            A = [[0 for _ in range(self.o[l])] for _ in range(self.o[l])]
            for k in range(self.o[l]):

                for i in range(self.o[l]):

                    I = self.O[l][i]

                    A[k][i] = self.gamma[l][k][I]

                    # Somar todos os coeficientes correspondentes à variável óleo x_i
                    for j in self.S[l]:
                        A[k][i] = self.K.Add(A[k][i], self.K.Multiply(self.alpha[l][k][j][i], x[j]))

            # self.alpha = [[[[rand.randint(0, self.order - 1) for _ in self.O[l]] for _ in self.S[l]] for
            #                                                   _ in range(self.o[l])] for l in range(self.u - 1)]
            # alpha[l][k][i][j] is the coefficient of oil-vinegar of layer l poly k

            SUM = lambda x, y: self.K.Add(x, y)
            SUB = lambda x, y: self.K.Subtract(x, y)
            PROD = lambda x, y: self.K.Multiply(x, y)
            DIV = lambda x, y: self.K.Divide(x, y)

            A_gm = gm.GenericMatrix(size=(self.o[l], self.o[l]), zeroElement=0, identityElement=1, add=SUM, mul=PROD,
                                    sub=SUB, div=DIV)

            for k in range(self.o[l]):
                A_gm.SetRow(k, A[k])

            A_inv = A_gm.Inverse()
            # print(self.o[l])
            # print(len(self.makeArrayFromMatrix(A_inv)))
            # print(len(Y))
            # return self.v
            X = self.matrixVectorProd(self.makeArrayFromMatrix(A_inv), Y)

            x[self.v[l]:self.v[l + 1]] = X

        x = self.matrixVectorProd(L2_inv, x)

        return x

    def makeArrayFromMatrix(self, matrix):
        n = matrix.Size()[0]
        matrixArray = [matrix.GetRow(i) for i in range(n)]
        return matrixArray

    def index(self, l, k):
        return (self.v[l] - self.v[0]) + k

    def sign(self, y):
        succeed = False
        while not succeed:
            try:
                x = self.findSolution(y)
                succeed = True
            except:
                succeed = False
        return x

    def verify(self, m, signature):
        return m == self.FTilde(signature)
