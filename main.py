# from rainbow import Rainbow
from announcements import Announcements
# from digital_signature import User

Announcer = Announcements.Announcements()


def manage(option):
    if option == "new user":
        name = input("name: ").rstrip("\n")
        if Announcer.isUser(name):  # if there is someone with that name already
            print("There is someone with that name already")
        else:
            password = input("password: ").rstrip("\n")
            Announcer.newUser(name, password)

    elif option == "see users":
        for user in Announcer.seeUsers():
            print(user)

    elif option == "log in":
        name = input("name: ").rstrip("\n")
        if not Announcer.isUser(name):
            print('I have no idea who daduck you are')
        else:
            password = input("password: ").rstrip("\n")
            if Announcer.logIn(name, password) != 0:
                print("hello ", name)
            else:
                print('wrong password')

    elif option == "log out":
        if not Announcer.log:
            print("You are not logged in you banana")
        else:
            print('bye ', Announcer.currentUser.name)
            Announcer.logOut()

    elif option == "announce":
        if Announcer.currentUser == 0:
            print('You are not logged in')
        else:
            title = input("title of the announcement: ").rstrip("\n")
            if Announcer.isAnnouncement(title):
                print("No")
            else:
                text = input("announcement: ").rstrip("\n")
                # print("signature: ", chr(a) for a in Announcer.makeAnnouncement(title, text)[])
                # print("signature: ", Announcer.makeAnnouncement(title, text))
                signature = Announcer.makeAnnouncement(title, text)
                k = len(signature)
                word = ""
                for i in range(k):
                    for j in signature[i]:
                        word += chr(j)
                print("signature: ", word)

    elif option == "verify":
        title = input("title of the announcement: ").rstrip("\n")
        if not Announcer.isAnnouncement(title):
            print('Not real')
        name = input("name of user: ").rstrip("\n")
        if not Announcer.isUser(name):
            print('Imaginary friend')
        print(Announcer.verifyAnnouncement(title, name))

    elif option == "see":
        announcement = input("title of the announcement: ").rstrip("\n")
        print(Announcer.seeAnnouncement(announcement))

    elif option == "see titles":
        for title in Announcer.seeAnnouncements():
            print(title)

    elif option == 'fake':
        title = input("title of the announcement: ").rstrip("\n")
        text = input("announcement: ").rstrip("\n")
        # print("signature: ", chr(a) for a in Announcer.makeAnnouncement(title, text)[])
        return False

    elif option == "help":
        print('The available commands are:')
        print(' - new user')
        print(' - log in')
        print(' - log out')
        print(' - see titles')
        print(' - see users')
        print(' - see')
        print(' - verify')
        print(' - announce')
        # print(' - fake')
        print(' - exit')

    else:
        print(option, 'is not a valid command.')
        print('Type help for a list of available commands.')


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


