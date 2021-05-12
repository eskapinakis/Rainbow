from rainbow import Rainbow


class User:

    name = ""
    password = ""
    rainbow = 0  # message size will be 33 - 6 = 27
    rainbowSize = 0

    def __init__(self, name='bob', password="banana"):
        self.name = name
        self.password = password
        self.rainbow = Rainbow.Rainbow(8)
        self.rainbowSize = self.rainbow.n - self.rainbow.v[0]
