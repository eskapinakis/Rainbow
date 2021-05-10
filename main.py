from rainbow import Rainbow


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    R = Rainbow.Rainbow(8)

    x = [2*i for i in range(R.n-R.v[0])]

    print( R.FTilde( R.findSolution(x) ) )
    print(R.verify(x,R.sign(x)))