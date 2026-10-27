from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QMessageBox, QComboBox)
from PyQt5.QtCore import Qt
from database.db_manager import DatabaseManager
from algorithms.scheduler import ScheduleGenerator


class ScheduleWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.db = DatabaseManager()
        self.setWindowTitle("Расписание колледжа")
        self.resize(1400, 800)
        self.setStyleSheet("background-color: #f0f2f5;")
        
        self._create_ui()
        self._load_schedule()
    
    def _create_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Заголовок
        if self.user['role'] == 'admin':
            title = QLabel("Расписание колледжа (Администратор)")
        else:
            title = QLabel(f"Расписание колледжа — {self.user['full_name']}")
        
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)
        
        # Кнопки управления
        btn_layout = QHBoxLayout()
        
        # Кнопка генерации только для админа
        if self.user['role'] == 'admin' or self.user.get('can_edit_schedule'):
            self.generate_btn = QPushButton("Составить автоматически")
            self.generate_btn.setStyleSheet("""
                QPushButton {
                    background-color: #27ae60;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 12px 24px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover { background-color: #219a52; }
            """)
            self.generate_btn.clicked.connect(self._generate_schedule)
            btn_layout.addWidget(self.generate_btn)
        
        # Фильтр по дням
        self.filter_combo = QComboBox()
        self.filter_combo.addItem("Все дни")
        self.filter_combo.addItems(['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'])
        self.filter_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
        """)
        self.filter_combo.currentTextChanged.connect(self._filter_schedule)
        btn_layout.addWidget(self.filter_combo)
        
        btn_layout.addStretch()
        
        self.back_btn = QPushButton("Назад")
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #7f8c8d; }
        """)
        self.back_btn.clicked.connect(self.close)
        btn_layout.addWidget(self.back_btn)
        
        layout.addLayout(btn_layout)
        
        # Таблица расписания (все видят всё)
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "День", "Время", "Неделя", "Предмет", 
            "Преподаватель", "Аудитория", "Группа"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.itemSelectionChanged.connect(self._on_row_selected)
        layout.addWidget(self.table)
        
        # Кнопки редактирования (только для своих пар)
        edit_layout = QHBoxLayout()
        
        if self.user['role'] == 'admin' or self.user.get('can_edit_schedule'):
            self.edit_btn = QPushButton("Редактировать выбранную")
            self.edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 10px 20px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover { background-color: #2980b9; }
            """)
            self.edit_btn.clicked.connect(self._edit_schedule)
            self.edit_btn.setEnabled(False)  # По умолчанию отключена
            edit_layout.addWidget(self.edit_btn)
            
            self.delete_btn = QPushButton("Удалить выбранную")
            self.delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 10px 20px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover { background-color: #c0392b; }
            """)
            self.delete_btn.clicked.connect(self._delete_schedule)
            self.delete_btn.setEnabled(False)
            edit_layout.addWidget(self.delete_btn)
        
        edit_layout.addStretch()
        layout.addLayout(edit_layout)
        
        # Статистика
        self.stats_label = QLabel("")
        self.stats_label.setStyleSheet("font-size: 14px; color: #7f8c8d; padding: 10px;")
        layout.addWidget(self.stats_label)
    
    def _load_schedule(self, day_filter=None):
        self.table.setRowCount(0)
        
        # ВСЕ видят полное расписание (без фильтрации по teacher_id)
        query = """
            SELECT s.id, s.day_of_week, s.time_slot, s.week_type, sub.name, 
                   u.full_name, c.number, g.name as group_name, s.teacher_id
            FROM schedule s
            JOIN subjects sub ON s.subject_id = sub.id
            JOIN users u ON s.teacher_id = u.id
            JOIN classrooms c ON s.classroom_id = c.id
            JOIN groups_table g ON s.group_id = g.id
        """
        params = []
        
        if day_filter and day_filter != "Все дни":
            query += " WHERE s.day_of_week = %s"
            params = [day_filter]
        
        query += " ORDER BY s.day_of_week, s.time_slot"
        
        rows = self.db.execute_query(query, params if params else None)
        
        for row_idx, row_data in enumerate(rows):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(row_data['id'])))
            self.table.setItem(row_idx, 1, QTableWidgetItem(row_data['day_of_week']))
            self.table.setItem(row_idx, 2, QTableWidgetItem(row_data['time_slot']))
            
            week_type = row_data.get('week_type') or 'both'
            week_display = {
                'both': 'Каждую',
                'numerator': 'Числитель',
                'denominator': 'Знаменатель'
            }.get(week_type, week_type)
            self.table.setItem(row_idx, 3, QTableWidgetItem(week_display))
            
            self.table.setItem(row_idx, 4, QTableWidgetItem(row_data['name']))
            self.table.setItem(row_idx, 5, QTableWidgetItem(row_data['full_name']))
            self.table.setItem(row_idx, 6, QTableWidgetItem(row_data['number']))
            self.table.setItem(row_idx, 7, QTableWidgetItem(row_data['group_name']))
            
            # Сохраняем teacher_id для проверки прав
            self.table.item(row_idx, 0).setData(Qt.UserRole, row_data['teacher_id'])
        
        self.stats_label.setText(f"Всего занятий: {len(rows)}")
    
    def _on_row_selected(self):
        """Проверяем, может ли пользователь редактировать выбранную строку"""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            if hasattr(self, 'edit_btn'):
                self.edit_btn.setEnabled(False)
                self.delete_btn.setEnabled(False)
            return
        
        # Получаем teacher_id из скрытых данных
        teacher_id = self.table.item(selected_row, 0).data(Qt.UserRole)
        
        # Админ может редактировать всё
        if self.user['role'] == 'admin' or self.user.get('can_edit_schedule'):
            if hasattr(self, 'edit_btn'):
                self.edit_btn.setEnabled(True)
                self.delete_btn.setEnabled(True)
        else:
            # Преподаватель может редактировать только свои пары
            if teacher_id == self.user['id']:
                if hasattr(self, 'edit_btn'):
                    self.edit_btn.setEnabled(True)
                    self.delete_btn.setEnabled(True)
            else:
                if hasattr(self, 'edit_btn'):
                    self.edit_btn.setEnabled(False)
                    self.delete_btn.setEnabled(False)
    
    def _edit_schedule(self):
        """Редактирование расписания (только для своих пар или админ)"""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите пару из таблицы!")
            return
        
        schedule_id = self.table.item(selected_row, 0).text()
        teacher_id = self.table.item(selected_row, 0).data(Qt.UserRole)
        
        # Проверка прав
        if self.user['role'] != 'admin' and teacher_id != self.user['id']:
            QMessageBox.warning(self, "Нет доступа", "Вы можете редактировать только свои пары!")
            return
        
        QMessageBox.information(self, "Информация", f"Редактирование пары ID: {schedule_id}\n(Функция в разработке)")
    
    def _delete_schedule(self):
        """Удаление пары из расписания"""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите пару из таблицы!")
            return
        
        schedule_id = self.table.item(selected_row, 0).text()
        teacher_id = self.table.item(selected_row, 0).data(Qt.UserRole)
        teacher_name = self.table.item(selected_row, 5).text()
        subject_name = self.table.item(selected_row, 4).text()
        
        # Проверка прав
        if self.user['role'] != 'admin' and teacher_id != self.user['id']:
            QMessageBox.warning(self, "Нет доступа", "Вы можете удалять только свои пары!")
            return
        
        reply = QMessageBox.question(
            self, "Подтверждение",
            f"Вы действительно хотите удалить пару?\n{subject_name} ({teacher_name})",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.db.execute_query("DELETE FROM schedule WHERE id = %s", (schedule_id,))
            QMessageBox.information(self, "Успех", "Пара удалена!")
            self._load_schedule()
    
    def _generate_schedule(self):
        """Автоматическая генерация расписания (только админ)"""
        if self.user['role'] != 'admin' and not self.user.get('can_edit_schedule'):
            QMessageBox.warning(self, "Нет доступа", "Только администратор может генерировать расписание")
            return
        
        generator = ScheduleGenerator()
        schedule, conflicts = generator.generate_schedule()
        generator.close()
        
        if conflicts:
            conflict_text = "\n".join(conflicts[:5])
            QMessageBox.warning(self, "Предупреждение", f"Не удалось назначить все часы:\n{conflict_text}")
        
        self._load_schedule()
        QMessageBox.information(self, "Успех", f"Расписание составлено! Назначено занятий: {len(schedule)}")
    
    def _filter_schedule(self, day):
        self._load_schedule(day)
    
    def closeEvent(self, event):
        self.db.close()
        event.accept()