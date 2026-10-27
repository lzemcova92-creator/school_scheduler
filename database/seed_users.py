import bcrypt
from database.db_manager import DatabaseManager

def seed_users():
    db = DatabaseManager()
    
    def hash_pwd(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Список пользователей: (username, password, full_name, role, can_edit, can_manage)
    users_data = [
        ('admin', 'admin123', 'Главный Администратор', 'admin', True, True),
        ('ayuvdji', '123456', 'Аювджи Ольга Владимировна', 'admin', True, True), # Второй админ
        
        ('talygina', '123456', 'Талыгина Ирина Геннадьевна', 'teacher', True, False),
        ('lahno_e', '123456', 'Лахно Екатерина Александровна', 'teacher', True, False),
        ('italyanceva', '123456', 'Итальянцева Виктория Михайловна', 'teacher', True, False),
        ('kostyukova', '123456', 'Костюкова Анна Валерьевна', 'teacher', True, False),
        ('shmarina', '123456', 'Шмарина Виктория Андреевна', 'teacher', True, False),
        ('lahno_d', '123456', 'Лахно Денис Дмитриевич', 'teacher', True, False),
        ('levina', '123456', 'Левина Любовь Михайловна', 'teacher', True, False),
        ('tomashev', '123456', 'Томашев Владислав Алексеевич', 'teacher', True, False),
        ('surogatova', '123456', 'Сурогатова Татьяна Васильевна', 'teacher', True, False),
        ('kobylinsky', '123456', 'Кобылинский Артем Павлович', 'teacher', True, False),
        ('vorontsova', '123456', 'Воронцова Ксения Олеговна', 'teacher', True, False),
        ('romashkov', '123456', 'Ромашков Антон Андреевич', 'teacher', True, False),
        ('kotikov', '123456', 'Котиков Вячеслав Михайлович', 'teacher', True, False),
        ('markilenko', '123456', 'Маркиленко Светлана Анатольевна', 'teacher', True, False),
    ]
    
    for u in users_data:
        try:
            db.execute_query(
                """INSERT INTO users (username, password_hash, full_name, role, can_edit_schedule, can_manage_users) 
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (u[0], hash_pwd(u[1]), u[2], u[3], u[4], u[5])
            )
            print(f"✅ Добавлен: {u[2]}")
        except Exception as e:
            print(f"⚠️ Пропущен (уже существует): {u[2]}")
            
    db.close()
    print("\n🎉 Пользователи успешно добавлены в облачную БД!")

if __name__ == '__main__':
    seed_users()