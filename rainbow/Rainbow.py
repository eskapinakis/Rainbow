# Class that implements Rainbow Signature Scheme
import random as rand  # to generate pseudo-random numbers
from pyfinite import ffield as ff  # to make calculations with field k of order 2^n
from pyfinite import genericmatrix as gm  # to make operations with matries in
import hashlib


class Rainbow:
    # Initializaion of variables
    K = 0  # Field K
    order = 0  # Number of elements in K
    n = 0  # Total number of variables
    u = 0  # Partition size
    v = []  # Numbers that create the partition
    S = []  # Vinegar variables of layer l: S[l]
    o = []  # Number of sublayers of layer l: o[l] = v[l+1] - v[l] for i in 1,..,u-1
    O = []  # Oil variables of layer l: O[l] = S[l+1]\S[l] for i in 1,..,u-1

    alpha = []  # alpha[l][k][i][j] is the coefficient of Oil-Vinegar of layer l poly k
    beta = []  # beta[l][k][i][j] is the coefficient of Vinegar-Vinegar of layer l poly k
    gamma = []  # gamma[l][k][i] is the linear term coefficient poly k
    eta = []  # eta[l][k] is the constant of each layer poly k

    L1 = []  # Invertible matrix of order (n-v[1], n-v[1])
    L2 = []  # Invertible matrix of order (n, n)

    publicKey = 0
    privateKey = 0

    def __init__(self, power, message_size=33, partition_size=6):

        # Create a field of size 2^power
        self.K = ff.FField(power)
        self.order = 2 ** power

        # Creates a random partition for the message space
        self.n = message_size  # The message size is actually n - v[0] = n-1 cause I can
        self.u = partition_size  # u-1 is also the number of Rainbow layers
        m = int(message_size / (partition_size - 1))
        self.v = [0] * partition_size
        self.v[0] = 6  # rand.randint(1, m)
        for i in range(1, self.u - 1):
            self.v[i] = rand.randint(self.v[i - 1] + 1, m * (i + 1) - 1)
        self.v[partition_size - 1] = self.n  # The last element has to equal the message size

        # Atribution of variables
        self.o = [self.v[l] - self.v[l - 1] for l in range(1, self.u)]
        self.S = [[i for i in range(v)] for v in self.v]
        self.O = [[j for j in range(self.v[i], self.v[i + 1])] for i in range(len(self.v) - 1)]

        self.alpha = [[[[rand.randint(0, self.order - 1) for _ in self.O[l]] for _ in self.S[l]] for
                       _ in range(self.o[l])] for l in range(self.u - 1)]

        self.beta = [[[[rand.randint(0, self.order - 1) for _ in self.S[l]] for _ in self.S[l]] for
                      _ in range(self.o[l])] for l in range(self.u - 1)]

        self.gamma = [[[rand.randint(0, self.order - 1) for _ in self.S[l + 1]] for _ in range(self.o[l])]
                      for l in range(self.u - 1)]

        self.eta = [[rand.randint(0, self.order - 1) for _ in range(self.o[l])] for l in range(self.u - 1)]

        self.L1 = self.invertibleMatrix(self.n - self.v[0])
        self.L2 = self.invertibleMatrix(self.n)

    # Multiplication of matrix by a vector
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

    # Creates a "random" invertible matrix of size n
    # Creates random and lower invertible triangular and multiplies them
    def invertibleMatrix(self, n):
        # Creation of Lower and Upper invertible matrices
        upper = [[0 for _ in range(n)] for _ in range(n)]
        lower = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i):
                upper[i][j] = rand.randint(0, self.order - 1)
                lower[n - i - 1][n - j - 1] = rand.randint(0, self.order - 1)
        for i in range(n):
            upper[i][i] = rand.randint(1, self.order - 1)
            lower[i][i] = rand.randint(1, self.order - 1)

        # Multiplication of upper and lower
        # Creation of lambda operations so we can multiply matrices with elements in the field
        SUM = lambda x, y: self.K.Add(x, y)
        SUB = lambda x, y: self.K.Subtract(x, y)
        PROD = lambda x, y: self.K.Multiply(x, y)
        DIV = lambda x, y: self.K.Divide(x, y)

        upper_gm = gm.GenericMatrix(size=(n, n), zeroElement=0, identityElement=1, add=SUM, mul=PROD, sub=SUB, div=DIV)
        for i in range(n):
            upper_gm.SetRow(i, upper[i])
        lower_gm = gm.GenericMatrix(size=(n, n), zeroElement=0, identityElement=1, add=SUM, mul=PROD, sub=SUB, div=DIV)
        for i in range(n):
            lower_gm.SetRow(i, lower[i])

        return upper_gm * lower_gm

    # Calculate de polynomial of layer l, sublayer k and entry x
    def poly(self, l, k, x):
        eval = self.eta[l][k]  # Constant term
        eval = self.K.Add(eval, self.oilVin(l, k, x))  # Oil-Vinegar terms
        eval = self.K.Add(eval, self.vinVin(l, k, x))  # Vinegar-Vinegar terms
        eval = self.K.Add(eval, self.linear(l, k, x))  # Linear terms
        return eval

    # Sum of Oil-Vinegar terms
    def oilVin(self, l, k, x):
        eval = 0
        for i in range(self.o[l]):
            for j in self.S[l]:
                I = self.O[l][i]
                var = self.K.Multiply(x[I], x[j])
                eval = self.K.Add(eval, self.K.Multiply(self.alpha[l][k][j][i], var))
        return eval

    # Sum of Vinegar-Vinegar terms
    def vinVin(self, l, k, x):
        eval = 0
        for i in self.S[l]:
            for j in self.S[l]:
                var = self.K.Multiply(x[i], x[j])
                eval = self.K.Add(eval, self.K.Multiply(self.beta[l][k][i][j], var))
        return eval

    # Sum of Linear terms
    def linear(self, l, k, x):
        eval = 0
        for i in self.S[l + 1]:
            eval = self.K.Add(eval, self.K.Multiply(self.gamma[l][k][i], x[i]))
        return eval

    # F: K^n -> K^{n-v[0]}
    # Returns array with n-v[0] values in k, the result of the n-v[0] polynomials
    def F(self, x):
        m = self.n - self.v[0]
        result = [0] * m  # (0,...,0)
        for l in range(self.u - 1):
            for k in range(self.o[l]):
                result[self.index(l, k)] = self.poly(l, k, x)
        return result

    # Applies L1 o F o L2 to x
    def FTilde(self, x):
        L2 = self.makeArrayFromMatrix(self.L2)
        L1 = self.makeArrayFromMatrix(self.L1)
        x = self.matrixVectorProd(L2, x)
        x = self.F(x)
        x = self.matrixVectorProd(L1, x)
        return x

        # Given y in k^(n-v[0])

    # Returns x in k^n solution to FTilde(x) = y
    # In other words, it calculates (L2^-1 o F^-1 o L1^-1)(y)
    def findSolution(self, y):
        # Calculate inverses of L1 and L2
        L2_inv = self.makeArrayFromMatrix(self.L2.Inverse())
        L1_inv = self.makeArrayFromMatrix(self.L1.Inverse())
        # Apply L1_inv to y
        y = self.matrixVectorProd(L1_inv, y)

        # Calculating "inverse" of F
        ####################################################################################################
        ####################################################################################################

        x = [0] * self.n  # The solution we are going to construct in parts
        # Guess the first v[0] elements
        for i in range(self.v[0]):
            x[i] = rand.randint(0, self.order - 1)

        # Resolution of the system of layer l
        for l in range(self.u - 1):
            # Y temporary of size o[l] to solve the system of layer l
            Y = y[self.v[l] - self.v[0]: self.v[l + 1] - self.v[0]]

            # k runs through all indices of sublayer of layer l
            for k in range(self.o[l]):
                # Passes all known terms to right side of the system
                Y[k] = self.K.Subtract(Y[k], self.eta[l][k])
                Y[k] = self.K.Subtract(Y[k], self.vinVin(l, k, x[0:self.v[l]]))

                temp = 0
                for p in self.S[l]:
                    temp = self.K.Add(temp, self.K.Multiply(self.gamma[l][k][p], x[p]))

                Y[k] = self.K.Subtract(Y[k], temp)

            # Create A coefficient matrix
            A = [[0 for _ in range(self.o[l])] for _ in range(self.o[l])]
            for k in range(self.o[l]):
                for i in range(self.o[l]):

                    I = self.O[l][
                        i]  # Index to access right index of gamma because gamma has coefficients for S[l+1] = S[l] U O[l]
                    A[k][i] = self.gamma[l][k][I]

                    # Sum all coefficients corresponding to Oil variable x_i
                    for j in self.S[l]:
                        A[k][i] = self.K.Add(A[k][i], self.K.Multiply(self.alpha[l][k][j][i], x[j]))

            # Calculating A_inv to solve the system
            SUM = lambda x, y: self.K.Add(x, y)
            SUB = lambda x, y: self.K.Subtract(x, y)
            PROD = lambda x, y: self.K.Multiply(x, y)
            DIV = lambda x, y: self.K.Divide(x, y)

            A_gm = gm.GenericMatrix(size=(self.o[l], self.o[l]), zeroElement=0, identityElement=1, add=SUM, mul=PROD,
                                    sub=SUB, div=DIV)

            for k in range(self.o[l]):
                A_gm.SetRow(k, A[k])

            A_inv = A_gm.Inverse()

            X = self.matrixVectorProd(self.makeArrayFromMatrix(A_inv), Y)  # Solution of the system of layer l

            x[self.v[l]:self.v[l + 1]] = X  # Add solution to the final solution
            ####################################################################################################
            ####################################################################################################

        x = self.matrixVectorProd(L2_inv, x)

        return x

    # Creates a 2D python array from a GM matrix
    def makeArrayFromMatrix(self, matrix):
        n = matrix.Size()[0]
        matrixArray = [matrix.GetRow(i) for i in range(n)]
        return matrixArray

    # Given layer l and sublayer k, returns general index
    def index(self, l, k):
        return (self.v[l] - self.v[0]) + k

    # Signing process
    def sign(self, y):
        # At some point in calculation of F^-1 the system may not have a solution
        # When that happens, guess other initial v[0] Vinegar variables
        # If the number of layers is not too high, we'll find a solution with high probability

        succeed = False
        while not succeed:
            try:
                x = self.findSolution(y)
                succeed = True
            except:
                succeed = False
        return x

    # Verifiyng authenticity process
    def verify(self, m, signature):
        return m == self.FTilde(signature)