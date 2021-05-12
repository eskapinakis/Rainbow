from rainbow import Rainbow
from digital_signature import Message


class User:

    name = ""
    password = ""
    rainbow = Rainbow.Rainbow(8)  # message size will be 33 - 6 = 27
    #  all the messages sent have to have the same size so decide now
    #  a message has the actual message, signature and the name of the user - [message, signature, user]
    messagesReceived = []

    def __init__(self, name='bob', password=0):
        self.name = name
        self.password = password

