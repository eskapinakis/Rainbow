# from rainbow import Rainbow
from digital_signature import SignatureManager
# from digital_signature import User

sm = SignatureManager.SignatureManager()


def manage(option):
    if option == "new user":
        name = input("name: ").rstrip("\n")
        password = input("password: ").rstrip("\n")
        if not sm.newUser(name, password):  # if there is someone with that name already
            print("There is someone with that name already")

    elif option == "see users":
        sm.seeUsers()

    elif option == "log in":
        name = input("name: ").rstrip("\n")
        if not sm.findUser(name):
            print('I have no idea who daduck you are')
        else:
            password = input("password: ").rstrip("\n")
            sm.logIn(name, password)
            if sm.currentUser != 0:
                print("hello ", name)
            else:
                print('wrong password')

    elif option == "log out":
        name = sm.currentUser.name
        sm.logOut()
        print('bye ', name)

    elif option == "send message":
        if sm.currentUser == 0:
            print('You are not logged in')
        else:
            sender = input("name of sender: ").rstrip("\n")
            receiver = input("name of receiver: ").rstrip("\n")
            message = input("message: ").rstrip("\n")
            sm.sendMessage(message, sender, receiver)

    elif option == "verify message":
        message = int(input("number of the message: ").rstrip("\n"))
        print(sm.verifyDocument(message))

    elif option == "current user":
        print(sm.currentUser.name)

    elif option == "see message":
        message = int(input("number of message: ").rstrip("\n"))
        print(sm.seeMessage(message))

    else:
        print(option, 'is not a valid command')


# returns a number for each letter
def getLetterCode(letter):
    if letter == ' ':
        return 26
    return ord(letter) - 97  # returns order of letter in the alphabet starting from 0..25


def getLetterFromCode(code):
    if code == 26:
        return ' '
    elif code == 27:
        return ''
    else:
        return chr(97+code)


if __name__ == '__main__':

    opt = input('Option: ').rstrip('\n')
    while opt != "exit":
        manage(opt)
        opt = input('Option: ').rstrip('\n')




    '''
    R = Rainbow.Rainbow(8)  # the message size is gonna be 27 = 33 - 6

    message = input("say message: ").rstrip('\n')
    m = len(message)
    rainbowSize = R.n - R.v[0]

    # if we just have to pad the message
    if m <= rainbowSize:
        y = [27]*rainbowSize  # 27 is the control character sort of
        for i in range(m):
            y[i] = getLetterCode(message[i])

        # try to sign the document - the matrix might not be invertible, hence the try
        invertible = False
        while not invertible:
            try:
                x = R.findSolution(y)
                invertible = True
            except ValueError:
                invertible = False
        # print(x)  # signature
        originalPadded = R.FTilde(x)
        original = ''
        for j in originalPadded:
            original += getLetterFromCode(j)
        print(original)  # original message
        print(R.verify(y, x))  # R.sign(y)))  # check if the signature is valid

    # if the message is bigger then we have to apply rainbow a bunch of times
    else:
        k = int(m/rainbowSize) + 1  # number of times we have to apply the rainbow
        y = [27] * rainbowSize * k  # gonna have the message plus the controls
        for i in range(m):
            y[i] = getLetterCode(message[i])  # fill y with the message leaving the controls at the end
        x = [0]*k
        for i in range(k):
            invertible = False
            while not invertible:
                try:
                    x[i] = R.findSolution(y[i*rainbowSize:(i+1)*rainbowSize])
                    invertible = True
                except ValueError:
                    invertible = False
        originalPadded = [0]*k
        original = ''
        for i in range(k):
            originalPadded[i] = R.FTilde(x[i])
            for j in originalPadded[i]:
                original += getLetterFromCode(j)
            # print([getLetterFromCode(i) for i in y[i*rainbowSize:(i+1)*rainbowSize]])
        print(original)  # original message
        verify = True
        for i in range(k):
            if not R.verify(y[i*rainbowSize:(i+1)*rainbowSize], x[i]):
                verify = False
                break
        print(verify)'''

    # hey i am a very very very very very very very very big message i think but im not really sure


