from announcements import User, Announcement


class Announcements:

    users = []
    announcements = {}
    currentUser = 0
    log = False

    def __init__(self):
        self.users = []
        self.currentUser = 0
        log = False

    def __findUser(self, user_name):
        for user in self.users:
            if user.name == user_name:
                return user
        return 0

    def isUser(self, name):
        return self.__findUser(name) != 0

    def newUser(self, name, password):
        if self.__findUser(name):
            return False
        newUser = User.User(name, password)
        self.users.append(newUser)
        return True

    def seeUsers(self):
        return [user.name for user in self.users]

    def logOut(self):
        self.currentUser = 0
        self.log = False

    def logIn(self, user_name, password):
        user = self.__findUser(user_name)
        if user.password == password:
            self.currentUser = user
            self.log = True
            return True
        return 0

    # signs a document/message with the right size
    def __signDocument(self, text):
        m = len(text)
        user = self.currentUser
        rainbowSize = user.rainbowSize
        signature = []
        # if we just have to pad the message
        if m <= rainbowSize:
            y = [27] * rainbowSize  # 27 is the control character sort of
            for i in range(m):
                y[i] = self.getLetterCode(text[i])  # turns text into an integers array
            # try to sign the document - the matrix might not be invertible, hence the try
            signature.append(user.rainbow.sign(y))
        else:
            k = int(m / rainbowSize) + 1  # number of times we have to apply the rainbow
            y = [27] * rainbowSize * k  # gonna have the message plus the controls
            for i in range(m):
                y[i] = self.getLetterCode(text[i])  # fill y with the message leaving the controls at the end
            for i in range(k):
                signature.append(user.rainbow.sign(y[i * rainbowSize:(i + 1) * rainbowSize]))
        return [y, signature]

    # checks if title is already a title of an announcement
    def isAnnouncement(self, title):
        return title in self.announcements.keys()

    # makes an announcement
    # the name can be your name or whatever you want you weirdo
    def makeAnnouncement(self, title, text):
        signature = self.__signDocument(text)
        announcement = Announcement.Announcement(self.currentUser.name, title, signature[0], signature[1])
        self.announcements[title] = announcement
        return signature[1]

    # see an announcement
    def seeAnnouncement(self, title):
        if not self.isAnnouncement(title):
            return False
        announcement = self.announcements[title]
        document = announcement.document
        text = ''
        for i in document:
            text += self.getLetterFromCode(i)
        return text

    # verifies if the name of the announcer is legit
    def verifyAnnouncement(self, title, name):
        announcement = self.announcements[title]
        document = announcement.document
        signature = announcement.signature
        user = self.__findUser(name)
        # return signature
        k = int(len(document) / user.rainbowSize + 0.5) # number of blocks
        n = user.rainbowSize
        # print('k: ', k)
        # print('size document: ', len(document))
        # print('n: ', n)
        # '''
        # if announcement.isSmallerThanRainbow:
        #    return user.rainbow.verify(document, signature[0])
        # else:
        for i in range(k):
            # print(user.rainbow.FTilde(signature[i]))
            # print('signature: ', signature[i])
            # print(len(signature[i]))
            # print('document: ', document[i*n:(i+1)*n])
            if not user.rainbow.verify(document[i*n:(i+1)*n], signature[i]):
                return False
            # print(user.rainbow.FTilde(signature[i]))
            # print(document)  #
        return True
        # '''

    def seeAnnouncements(self):
        return list(self.announcements.keys())

    # returns a number for each letter
    @staticmethod
    def getLetterCode(letter):
        if letter == ' ':
            return 26
        return ord(letter) - 97  # returns order of letter in the alphabet starting from 0..25

    @staticmethod
    def getLetterFromCode(code):
        if code == 26:
            return ' '
        elif code == 27:
            return ''
        else:
            return chr(97 + code)
