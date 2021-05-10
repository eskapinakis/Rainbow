from digital_signature import User
from digital_signature import Message


class SignatureManager:

    users = []
    currentUser = 0

    def __init__(self):
        self.users = []
        self.currentUser = 0

    def newUser(self, user_name, message_size):
        newUser = User.User(user_name, message_size)
        self.users.append(newUser)

    def logOut(self):
        self.currentUser = 0

    def logIn(self, user_name):
        self.currentUser = self.findUser(user_name)

    def findUser(self, user_name):
        for user in self.users:
            if user.name == user_name:
                return user

    def sendMessage(self, m, user_name):
        user = self.findUser(user_name)
        signature = self.signDocument(m)
        message = Message.Message(self.currentUser.name, user_name, m, signature)
        user.messagesReceived.append(message)
        self.currentUser.messagesSent.append(message)

    # signs a document/message with the right size
    def signDocument(self, m):
        x = self.currentUser.rainbow.sign(m)
        # print(self.currentUser.rainbow.FTilde(x))
        return x

    # verifies a message sent from another guy
    def verifyDocument(self, m):
        message = self.currentUser.messagesReceived[m]
        user = self.findUser(message.sender)
        signature = message.signature
        text = message.message
        return user.rainbow.verify(text, signature)

    # send message to user
    #def sendMessage(self, m, user_name):
    #    user = self.findUser(user_name)
    #    user.messagesReceived += [m, self.signDocument(m)]

    def seeUsers(self):
        for user in self.users:
            print(user.name)
