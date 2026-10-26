import bcrypt
from database.db_manager import DatabaseManager


def seed_database():
    """Заполнение БД тестовыми данными (20-30 записей)"""
    db = DatabaseManager()
    
    # Хэширование пароля
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # 1. Пользователи (админ + преподаватели) — 8 записей
    users = [
        ('admin', hash_password('admin123'), 'Администратор Системы', 'admin'),
        ('ivanov', hash_password('123456'), 'Иванов Иван Иванович', 'teacher'),
        ('petrova', hash_password('123456'), 'Петрова Мария Сергеевна', 'teacher'),
        ('sidorov', hash_password('123456'), 'Сидоров Алексей Петрович', 'teacher'),
        ('smirnova', hash_password('123456'), 'Смирнова Ольга Николаевна', 'teacher'),
        ('kozlov', hash_password('123456'), 'Козлов Дмитрий Владимирович', 'teacher'),
        ('novikova', hash_password('123456'), 'Новикова Анна Павловна', 'teacher'),
        ('volkov', hash_password('123456'), 'Волков Сергей Александрович', 'teacher'),
    ]
    
    for u in users:
        try:
            db.execute_query(
                "INSERT INTO users (username, password_hash, full_name, role) VALUES (?, ?, ?, ?)",
                u
            )
        except Exception:
            pass  # если уже есть — пропускаем
    
    # 2. Предметы — 10 записей
    subjects = [
        ('Математика', 2, 2),    # teacher_id=2 (Иванов)
        ('Алгебра', 3, 2),       # teacher_id=2
        ('Физика', 4, 2),        # teacher_id=3 (Петрова)
        ('Химия', 5, 2),         # teacher_id=4 (Сидоров)
        ('Биология', 6, 2),      # teacher_id=5 (Смирнова)
        ('История', 7, 2),       # teacher_id=6 (Козлов)
        ('Литература', 8, 2),    # teacher_id=7 (Новикова)
        ('Английский язык', 9, 2),  # teacher_id=8 (Волков)
        ('Информатика', 2, 2),   # teacher_id=2
        ('География', 3, 2),     # teacher_id=3
    ]
    
    for s in subjects:
        try:
            db.execute_query(
                "INSERT INTO subjects (name, teacher_id, hours_per_week) VALUES (?, ?, ?)",
                s
            )
        except Exception:
            pass
    
    # 3. Аудитории — 10 записей
    classrooms = [
        ('101', 30, 'Проектор, доска', 'Главный корпус'),
        ('102', 25, 'Проектор', 'Главный корпус'),
        ('201', 30, 'Компьютеры, проектор', 'Главный корпус'),
        ('202', 25, 'Доска', 'Главный корпус'),
        ('301', 20, 'Лабораторное оборудование', 'Лабораторный корпус'),
        ('302', 20, 'Лабораторное оборудование', 'Лабораторный корпус'),
        ('401', 35, 'Спортзал', 'Спортивный корпус'),
        ('402', 30, 'Актовый зал', 'Главный корпус'),
        ('103', 28, 'Проектор, доска', 'Главный корпус'),
        ('203', 22, 'Библиотека', 'Главный корпус'),
    ]
    
    for c in classrooms:
        try:
            db.execute_query(
                "INSERT INTO classrooms (number, capacity, equipment, building) VALUES (?, ?, ?, ?)",
                c
            )
        except Exception:
            pass
    
    db.close()
    print("✅ База данных заполнена тестовыми данными!")


if __name__ == '__main__':
    seed_database()