from database.db_manager import DatabaseManager

db = DatabaseManager()

print("=== Добавляем аудитории ===")

# Список аудиторий
classrooms = [
    (101, 30, 'Доска, проектор'),
    (102, 25, 'Доска'),
    (201, 30, 'Доска, проектор, компьютеры'),
    (202, 20, 'Доска'),
    (301, 35, 'Доска, проектор'),
    (302, 25, 'Доска, компьютеры'),
    (401, 30, 'Доска, проектор'),
    (402, 20, 'Доска'),
    (501, 35, 'Доска, проектор'),
    (502, 25, 'Доска, компьютеры'),
]

for classroom in classrooms:
    try:
        db.execute_query(
            "INSERT INTO classrooms (number, capacity, equipment) VALUES (?, ?, ?)",
            classroom
        )
        print(f"  Добавлена аудитория {classroom[0]} (вместимость: {classroom[1]})")
    except Exception as e:
        print(f"  Ошибка при добавлении аудитории {classroom[0]}: {e}")

print(f"\nВсего добавлено аудиторий: {len(classrooms)}")

# Проверяем результат
result = db.execute_query("SELECT id, number, capacity FROM classrooms")
print(f"\n=== Проверка ===")
for c in result:
    print(f"  ID: {c['id']}, Номер: {c['number']}, Вместимость: {c['capacity']}")
print(f"Всего аудиторий в базе: {len(result)}")

db.close()