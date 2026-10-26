from database.db_manager import DatabaseManager

db = DatabaseManager()

print("=== Пользователи (преподаватели) ===")
users = db.execute_query("SELECT id, username, full_name, role FROM users WHERE role = 'teacher'")
for u in users:
    print(f"  ID: {u['id']}, Логин: {u['username']}, ФИО: {u['full_name']}")
print(f"Всего преподавателей: {len(users)}\n")

print("=== Предметы ===")
subjects = db.execute_query("SELECT id, name, teacher_id, hours_per_week FROM subjects")
for s in subjects:
    print(f"  ID: {s['id']}, Название: {s['name']}, Преподаватель ID: {s['teacher_id']}, Часов: {s['hours_per_week']}")
print(f"Всего предметов: {len(subjects)}\n")

print("=== Аудитории ===")
classrooms = db.execute_query("SELECT id, number, capacity, equipment FROM classrooms")
for c in classrooms:
    print(f"  ID: {c['id']}, Номер: {c['number']}, Вместимость: {c['capacity']}")
print(f"Всего аудиторий: {len(classrooms)}\n")

db.close()