class Announcement:

    # name = 0
    userName = 0
    title = 0
    document = 0
    signature = 0
    isSmallerThanRainbow = False

    def __init__(self, user_name, title, document, signature, is_smaller_than_rainbow=False):
        self.title = title
        self.userName = user_name
        self.document = document
        self.signature = signature
        self.isSmallerThanRainbow = is_smaller_than_rainbow