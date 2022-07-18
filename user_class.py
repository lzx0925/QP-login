class User:
    def __init__(self):
        self.name = ''
        self.key = ''
        self.email = ''

    def get_info(self, username, password, email):
        self.name = username
        self.key = password
        self.email = email
