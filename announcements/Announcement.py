# Class that has the atributes for an announcement

class Announcement:

    userName = 0
    title = 0
    document = 0
    signature = 0

    def __init__(self, user_name, title, document, signature):
        self.title = title
        self.userName = user_name
        self.document = document
        self.signature = signature