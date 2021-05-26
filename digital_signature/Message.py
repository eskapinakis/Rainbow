class Message:

    sender = 0
    receiver = 0
    text = 0
    signature = 0
    isSmallerThanRainbow = False

    def __init__(self, sender, receiver, text, signature, is_smaller_than_rainbow=False):
        self.sender = sender
        self.receiver = receiver
        self.text = text
        self.signature = signature
        self.isSmallerThanRainbow = is_smaller_than_rainbow