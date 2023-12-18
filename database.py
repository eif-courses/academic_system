import sqlite3
from sqlite3 import Error


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
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                user_type TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS lecturers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            );

            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            );

            CREATE TABLE IF NOT EXISTS enrollments (
                student_id INTEGER NOT NULL,
                subject_id INTEGER NOT NULL,
                PRIMARY KEY (student_id, subject_id),
                FOREIGN KEY (student_id) REFERENCES students (id),
                FOREIGN KEY (subject_id) REFERENCES subjects (id)
            );

            CREATE TABLE IF NOT EXISTS grades (
                student_id INTEGER NOT NULL,
                subject_id INTEGER NOT NULL,
                grade INTEGER NOT NULL,
                PRIMARY KEY (student_id, subject_id),
                FOREIGN KEY (student_id) REFERENCES students (id),
                FOREIGN KEY (subject_id) REFERENCES subjects (id)
            );
        """
        try:
            cursor = self.connection.cursor()
            cursor.executescript(schema_query)
        except Error as e:
            print(e)
