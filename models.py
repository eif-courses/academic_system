class User:
    def __init__(self, username, password, role):
        self.id = None
        self.username = username
        self.password = password
        self.role = role


class StudentGroup:
    def __init__(self, group_name):
        self.id = None
        self.group_name = group_name


class Course:
    def __init__(self, course_name):
        self.id = None
        self.course_name = course_name


class Subject:
    def __init__(self, subject_name):
        self.id = None
        self.subject_name = subject_name


class Lecturer:
    def __init__(self, lecturer_name, username, password):
        self.id = None
        self.lecturer_name = lecturer_name
        self.username = username
        self.password = password


class Student:
    def __init__(self, student_name, username, password):
        self.id = None
        self.student_name = student_name
        self.username = username
        self.password = password