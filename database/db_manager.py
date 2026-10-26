import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name='school.db'):
        # База данных будет создана в папке database
        self.db_path = os.path.join(os.path.dirname(__file__), db_name)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.executescript('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin', 'teacher'))
            );

            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                teacher_id INTEGER,
                hours_per_week INTEGER DEFAULT 2,
                FOREIGN KEY (teacher_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS classrooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number TEXT UNIQUE NOT NULL,
                capacity INTEGER NOT NULL,
                equipment TEXT
            );

            CREATE TABLE IF NOT EXISTS schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_id INTEGER NOT NULL,
                classroom_id INTEGER NOT NULL,
                teacher_id INTEGER NOT NULL,
                day_of_week TEXT NOT NULL,
                time_slot TEXT NOT NULL,
                group_name TEXT NOT NULL,
                FOREIGN KEY (subject_id) REFERENCES subjects(id),
                FOREIGN KEY (classroom_id) REFERENCES classrooms(id),
                FOREIGN KEY (teacher_id) REFERENCES users(id),
                UNIQUE(day_of_week, time_slot, classroom_id),
                UNIQUE(day_of_week, time_slot, teacher_id)
            );
        ''')
        self.conn.commit()

    def execute_query(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.conn.commit()
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()