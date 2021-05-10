from rainbow import Rainbow
from digital_signature import Message


class User:

    rainbow = 0
    name = ""
    #  all the messages sent have to have the same size so decide now
    #  a message has the actual message, signature and the name of the user - [message, signature, user]
    messagesReceived = []
    messagesSent = []
    messageSize = 0

    def __init__(self, name, message_size):
        self.name = name
        self.messageSize = message_size
        self.rainbow = Rainbow.Rainbow(8, message_size+1, 6)  # +1 because you take 1 in the rainbow

