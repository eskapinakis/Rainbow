from digital_signature import User
from digital_signature import Message
from rainbow import Rainbow


class SignatureManager:

    users = []
    currentUser = 0

    # these two don't really do anything it's just for information
    rainbow = 0
    rainbowSize = 0

    def __init__(self):
        self.rainbow = Rainbow.Rainbow(8)  # message size will be 33 - 6 = 27
        self.rainbowSize = self.rainbow.n - self.rainbow.v[0]
        self.users = []
        self.currentUser = 0

    def newUser(self, user_name, password):
        if self.findUser(user_name):
            return False
        newUser = User.User(name=user_name, password=password)
        self.users.append(newUser)
        return True

    def logOut(self):
        self.currentUser = 0

    def logIn(self, user_name, password):
        user = self.findUser(user_name)
        if user.password == password:
            self.currentUser = user

    def findUser(self, user_name):
        for user in self.users:
            if user.name == user_name:
                return user

    def sendMessage(self, msg, sender, receiver):
        userReceiver = self.findUser(receiver)
        m = len(msg)
        # if we just have to pad the message
        if m <= self.rainbowSize:
            y = [27] * self.rainbowSize  # 27 is the control character sort of
            for i in range(m):
                y[i] = self.getLetterCode(msg[i])
            # try to sign the document - the matrix might not be invertible, hence the try
            signature = self.signDocument(y)
        else:
            k = int(m / self.rainbowSize) + 1  # number of times we have to apply the rainbow
            y = [27] * self.rainbowSize * k  # gonna have the message plus the controls
            for i in range(m):
                y[i] = self.getLetterCode(msg[i])  # fill y with the message leaving the controls at the end
            signature = [0] * k
            for i in range(k):
                signature[i] = self.signDocument(y[i * self.rainbowSize:(i + 1) * self.rainbowSize])
        message = Message.Message(sender, receiver, y, signature, m <= self.rainbowSize)
        userReceiver.messagesReceived.append(message)

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

    # signs a document/message with the right size
    def signDocument(self, m):
        x = self.currentUser.rainbow.sign(m)
        # print(self.currentUser.rainbow.FTilde(x))
        return x

    # verifies a message sent from another guy
    def verifyDocument(self, message_index):
        message = self.currentUser.messagesReceived[message_index]
        user = self.findUser(message.sender)
        signature = message.signature
        text = message.text
        if message.isSmallerThanRainbow:
            return user.rainbow.verify(text, signature)
        else:
            k = int(len(text) / self.rainbowSize) + 1
            for i in range(k):
                if not user.rainbow.verify(text[i * self.rainbowSize:(i + 1) * self.rainbowSize], signature[i]):
                    return False
            return True

    # send message to user
    def seeMessage(self, m):
        msg = self.currentUser.messagesReceived[m]
        original = ''
        if msg.isSmallerThanRainbow:
            for j in msg.text:
                original += self.getLetterFromCode(j)
        else:
            original = 'a'
        return original

    def seeUsers(self):
        for user in self.users:
            print(user.name)
