from rainbow import Rainbow
from digital_signature import SignatureManager
from digital_signature import User

sm = SignatureManager.SignatureManager()


def manage(option, sm):
    if option == "new user":
        name = input("name: ").rstrip("\n")
        password = input("password: ").rstrip("\n")
        ms = int(input("message size: ").rstrip("\n"))
        sm.newUser(name, ms, password)

    elif option == "see users":
        sm.seeUsers()

    elif option == "log in":
        name = input("name: ").rstrip("\n")
        password = input("password: ").rstrip("\n")
        sm.logIn(name, password)
        if sm.currentUser != 0:
            print("hello ", name)

    elif option == "log out":
        name = sm.currentUser.name
        sm.logOut()
        print('bye ', name)

    elif option == "send message":
        name = input("name of user: ").rstrip("\n")
        message = input("message: ").rstrip("\n")
        m = [0]*sm.currentUser.messageSize
        for i in range(len(message)):
            m[i] = int(message[i])
        sm.sendMessage(m, name)

    elif option == "verify message":
        message = int(input("message: ").rstrip("\n"))
        print(sm.verifyDocument(message))

    elif option == "current user":
        print(sm.currentUser.name)

    else:
        print(option, 'is not a valid command')


if __name__ == '__main__':
    '''R = Rainbow.Rainbow(8, 40, 6)

    y = [i for i in range(R.n - R.v[0])]

    x = R.findSolution(y)
    print(R.FTilde(x))
    print(R.verify(y, R.sign(y)))'''

    option = input("option: ").rstrip("\n")
    while option != "exit":
        manage(option, sm)
        option = input("option: ").rstrip("\n")


