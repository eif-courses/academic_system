import sqlite3
from sqlite3 import Error

from models import User, StudentGroup, Course, Subject, Lecturer, Student


class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = self.create_connection()

    def create_connection(self):
        try:
            connection = sqlite3.connect(self.db_file, isolation_level=None)
            return connection
        except Error as e:
            print(e)

    def close_connection(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return cursor.lastrowid
        except Error as e:
            print(e)

    def fetch_all(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print(e)

    def create_tables(self):
        schema_query = """
        -- Create Users table
        CREATE TABLE IF NOT EXISTS Users (
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            Username TEXT NOT NULL,
            Password TEXT NOT NULL,
            Role TEXT NOT NULL
        );
        
        -- Create StudentGroups table
        CREATE TABLE IF NOT EXISTS StudentGroups (
            GroupID INTEGER PRIMARY KEY AUTOINCREMENT,
            GroupName TEXT NOT NULL
        );
        
        -- Create Courses table
        CREATE TABLE IF NOT EXISTS Courses (
            CourseID INTEGER PRIMARY KEY AUTOINCREMENT,
            CourseName TEXT NOT NULL
        );
        
        -- Create Subjects table
        CREATE TABLE IF NOT EXISTS Subjects (
            SubjectID INTEGER PRIMARY KEY AUTOINCREMENT,
            SubjectName TEXT NOT NULL
        );
        
        -- Create Lecturers table
        CREATE TABLE IF NOT EXISTS Lecturers (
            LecturerID INTEGER PRIMARY KEY AUTOINCREMENT,
            LecturerName TEXT NOT NULL,
            UserID INTEGER NOT NULL,
            FOREIGN KEY (UserID) REFERENCES Users(UserID)
        );
        
        -- Create Students table
        CREATE TABLE IF NOT EXISTS Students (
            StudentID INTEGER PRIMARY KEY AUTOINCREMENT,
            StudentName TEXT NOT NULL,
            UserID INTEGER NOT NULL,
            GroupID INTEGER,
            FOREIGN KEY (UserID) REFERENCES Users(UserID),
            FOREIGN KEY (GroupID) REFERENCES StudentGroups(GroupID)
        );
        
        -- Create Enrollments table
        CREATE TABLE IF NOT EXISTS Enrollments (
            StudentID INTEGER NOT NULL,
            SubjectID INTEGER NOT NULL,
            PRIMARY KEY (StudentID, SubjectID),
            FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
            FOREIGN KEY (SubjectID) REFERENCES Subjects(SubjectID)
        );
        
        -- Create Grades table
        CREATE TABLE IF NOT EXISTS Grades (
            StudentID INTEGER NOT NULL,
            SubjectID INTEGER NOT NULL,
            Grade INTEGER NOT NULL,
            PRIMARY KEY (StudentID, SubjectID),
            FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
            FOREIGN KEY (SubjectID) REFERENCES Subjects(SubjectID)
        );
     """
        try:
            cursor = self.connection.cursor()
            cursor.executescript(schema_query)
        except Error as e:
            print(e)

    # Function to create an administrator user
    def create_admin_user(self, db):
        admin_user = User("admin", "admin_password", "administrator")
        admin_user.id = db.execute_query("INSERT INTO Users (Username, Password, Role) VALUES (?, ?, ?)",
                                         (admin_user.username, admin_user.password, admin_user.role))
        return admin_user

    # Function to create a student group

    def create_student_group(self, db, group_name):
        group = StudentGroup(group_name)
        group.id = db.execute_query("INSERT INTO StudentGroups (GroupName) VALUES (?)", (group.group_name,))
        return group

    # Function to create a course

    def create_course(self, db, course_name):
        course = Course(course_name)
        course.id = db.execute_query("INSERT INTO Courses (CourseName) VALUES (?)", (course.course_name,))
        return course

    # Function to create a subject
    def create_subject(self, db, subject_name):
        subject = Subject(subject_name)
        subject.id = db.execute_query("INSERT INTO Subjects (SubjectName) VALUES (?)", (subject.subject_name,))
        return subject

    # Function to create a lecturer

    def create_lecturer(self, db, lecturer_name, username, password, admin_user_id):
        lect = Lecturer(lecturer_name, username, password)
        lect.id = db.execute_query("INSERT INTO Lecturers (LecturerName, UserID) VALUES (?, ?)",
                                   (lect.lecturer_name, admin_user_id))
        return lect

    # Function to create a student

    def create_student(self, db, student_name, username, password, admin_user_id, group_id):
        stud = Student(student_name, username, password)
        stud.id = db.execute_query("INSERT INTO Students (StudentName, UserID, GroupID) VALUES (?, ?, ?)",
                                   (stud.student_name, admin_user_id, group_id))
        return stud

    # Function to enroll a student in a subject

    def enroll_student_in_subject(self, db, student_id, subject_id):
        db.execute_query("INSERT INTO Enrollments (StudentID, SubjectID) VALUES (?, ?)", (student_id, subject_id))

    # Function to enter a grade for a student

    def enter_grade_for_student(self, db, student_id, subject_id, grade):
        db.execute_query("INSERT INTO Grades (StudentID, SubjectID, Grade) VALUES (?, ?, ?)",
                         (student_id, subject_id, grade))
