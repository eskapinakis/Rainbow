class Message:

    sender = 0
    receiver = 0
    message = 0
    signature = 0

    def __init__(self, sender, receiver, message, signature):
        self.sender = sender
        self.receiver = receiver
        self.message = message
        self.signature = signature