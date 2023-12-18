class User:
    def __init__(self, username, password, user_type):
        self.id = None
        self.username = username
        self.password = password
        self.user_type = user_type


class Administrator(User):
    def __init__(self, username, password):
        super().__init__(username, password, "administrator")


class Lecturer(User):
    def __init__(self, username, password, name):
        super().__init__(username, password, "lecturer")
        self.name = name


class Student(User):
    def __init__(self, username, password, name):
        super().__init__(username, password, "student")
        self.name = name


class Group:
    def __init__(self, name):
        self.id = None
        self.name = name


class Course:
    def __init__(self, name):
        self.id = None
        self.name = name


class Subject:
    def __init__(self, name):
        self.id = None
        self.name = name
