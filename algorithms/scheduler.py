from database.db_manager import DatabaseManager


class ScheduleGenerator:
    def __init__(self):
        self.db = DatabaseManager()
        self.schedule = []
        self.conflicts = []
    
    def generate_schedule(self):
        """Автоматическая генерация расписания"""
        # Очищаем старое расписание
        self.db.execute_query("DELETE FROM schedule")
        self.schedule = []
        self.conflicts = []
        
        # Получаем данные
        subjects = self.db.execute_query("""
            SELECT s.id, s.name, s.teacher_id, s.hours_per_week, u.full_name as teacher_name
            FROM subjects s
            JOIN users u ON s.teacher_id = u.id
        """)
        
        classrooms = self.db.execute_query("SELECT id, number, capacity FROM classrooms")
        
        # Дни и время
        days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт']
        time_slots = ['08:30-09:15', '09:25-10:10', '10:20-11:05', '11:15-12:00', 
                      '12:20-13:05', '13:15-14:00', '14:10-14:55']
        
        groups = ['5А', '5Б', '6А', '6Б', '7А', '7Б', '8А', '8Б', '9А', '9Б', '10А', '10Б', '11А', '11Б']
        
        # Для каждого предмета пытаемся назначить уроки
        for subject in subjects:
            hours_needed = subject['hours_per_week']
            hours_assigned = 0
            
            for day in days:
                if hours_assigned >= hours_needed:
                    break
                
                for time_slot in time_slots:
                    if hours_assigned >= hours_needed:
                        break
                    
                    # Проверяем конфликты
                    if self._has_conflict(subject['teacher_id'], day, time_slot):
                        continue
                    
                    # Выбираем аудиторию
                    classroom = self._find_available_classroom(day, time_slot, classrooms)
                    if not classroom:
                        continue
                    
                    # Выбираем группу
                    group = groups[hours_assigned % len(groups)]
                    
                    # Добавляем в расписание
                    self.db.execute_query(
                        """INSERT INTO schedule 
                           (subject_id, classroom_id, teacher_id, day_of_week, time_slot, group_name) 
                           VALUES (?, ?, ?, ?, ?, ?)""",
                        (subject['id'], classroom['id'], subject['teacher_id'], day, time_slot, group)
                    )
                    
                    self.schedule.append({
                        'subject': subject['name'],
                        'teacher': subject['teacher_name'],
                        'classroom': classroom['number'],
                        'day': day,
                        'time': time_slot,
                        'group': group
                    })
                    
                    hours_assigned += 1
            
            if hours_assigned < hours_needed:
                self.conflicts.append(f"Предмет '{subject['name']}': назначено {hours_assigned} из {hours_needed} часов")
        
        return self.schedule, self.conflicts
    
    def _has_conflict(self, teacher_id, day, time_slot):
        """Проверка конфликта: преподаватель уже занят в это время"""
        result = self.db.execute_query(
            "SELECT id FROM schedule WHERE teacher_id = ? AND day_of_week = ? AND time_slot = ?",
            (teacher_id, day, time_slot)
        )
        return len(result) > 0
    
    def _find_available_classroom(self, day, time_slot, classrooms):
        """Поиск свободной аудитории"""
        for classroom in classrooms:
            result = self.db.execute_query(
                "SELECT id FROM schedule WHERE classroom_id = ? AND day_of_week = ? AND time_slot = ?",
                (classroom['id'], day, time_slot)
            )
            if len(result) == 0:
                return classroom
        return None
    
    def close(self):
        self.db.close()