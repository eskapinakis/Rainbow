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
            Announcer.newUser(name, password)  # add user

    elif option == "see users":
        for user in Announcer.seeUsers():
            print(user)

    elif option == "log in":
        name = input("name: ").rstrip("\n")
        if not Announcer.isUser(name):   # if there is no user with that name
            print('I have no idea who daduck you are')
        else:
            password = input("password: ").rstrip("\n")
            if Announcer.logIn(name, password) != 0:
                print("hello", name)
            else:
                print('wrong password')  # wrong password

    elif option == "log out":
        if not Announcer.log:    # if no one is logged in
            print("You are not logged in")
        else:
            print("bye", Announcer.currentUser.name)
            Announcer.logOut()

    elif option == "announce":    # to create announcements and sign them
        if Announcer.currentUser == 0:   # if no one is logged in
            print('You are not logged in')
        else:
            title = input("title of the announcement: ").rstrip("\n")  # entry the announcement title
            if Announcer.isAnnouncement(title):
                print("No")
            else:
                text = input("announcement: ").rstrip("\n")  # text of the announcement
                signature = Announcer.makeAnnouncement(title, text)
                k = len(signature)
                word = ""
                for i in range(k):
                    for j in signature[i]:
                        word += chr(j)
                print("signature: ", word)

    elif option == "verify":   
        title = input("title of the announcement: ").rstrip("\n")  # get announcement title
        if not Announcer.isAnnouncement(title):
            print('Not real')
        name = input("name of user: ").rstrip("\n")   # get user name to verify
        if not Announcer.isUser(name):    # if the user does not exist
            print('Imaginary friend')
        else:
            print(Announcer.verifyAnnouncement(title, name))

    elif option == "see ann":  # see announcements
        announcement = input("title of the announcement: ").rstrip("\n")
        var = Announcer.seeAnnouncement(announcement)
        print('----------------------------------')
        print("title: ", var[1])
        print(var[0])
        print("signature: ", var[2])
        print('----------------------------------')

    elif option == "see titles":
        for title in Announcer.seeAnnouncements():
            print(title)

    elif option == "help":
        print('The available commands are:')
        print(' - new user')
        print(' - log in')
        print(' - log out')
        print(' - see titles')
        print(' - see users')
        print(' - see ann')
        print(' - verify')
        print(' - announce')
        print(' - exit')

    else:
        print(option, 'is not a valid command.')
        print('Type help for a list of available commands.')


if __name__ == '__main__':

    opt = input('Option: ').rstrip('\n')
    while opt != "exit":
        manage(opt)
        opt = input('Option: ').rstrip('\n')
