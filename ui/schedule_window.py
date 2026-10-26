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
        self.setWindowTitle("Расписание")
        self.resize(1200, 700)
        self.setStyleSheet("background-color: #f0f2f5;")
        
        self._create_ui()
        self._load_schedule()
    
    def _create_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        title = QLabel("Расписание занятий")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)
        
        # Кнопки управления
        btn_layout = QHBoxLayout()
        
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
            QPushButton:hover {
                background-color: #219a52;
            }
        """)
        self.generate_btn.clicked.connect(self._generate_schedule)
        btn_layout.addWidget(self.generate_btn)
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItem("Все дни")
        self.filter_combo.addItems(['Пн', 'Вт', 'Ср', 'Чт', 'Пт'])
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
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        self.back_btn.clicked.connect(self.close)
        btn_layout.addWidget(self.back_btn)
        
        layout.addLayout(btn_layout)
        
        # Таблица расписания
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["День", "Время", "Предмет", "Преподаватель", "Аудитория", "Группа"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)
        
        # Статистика
        self.stats_label = QLabel("")
        self.stats_label.setStyleSheet("font-size: 14px; color: #7f8c8d; padding: 10px;")
        layout.addWidget(self.stats_label)
    
    def _load_schedule(self, day_filter=None):
        self.table.setRowCount(0)
        
        query = """
            SELECT s.day_of_week, s.time_slot, sub.name, u.full_name, c.number, s.group_name
            FROM schedule s
            JOIN subjects sub ON s.subject_id = sub.id
            JOIN users u ON s.teacher_id = u.id
            JOIN classrooms c ON s.classroom_id = c.id
        """
        
        if day_filter and day_filter != "Все дни":
            query += f" WHERE s.day_of_week = '{day_filter}'"
        
        query += " ORDER BY s.day_of_week, s.time_slot"
        
        rows = self.db.execute_query(query)
        
        for row_idx, row_data in enumerate(rows):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(row_data['day_of_week']))
            self.table.setItem(row_idx, 1, QTableWidgetItem(row_data['time_slot']))
            self.table.setItem(row_idx, 2, QTableWidgetItem(row_data['name']))
            self.table.setItem(row_idx, 3, QTableWidgetItem(row_data['full_name']))
            self.table.setItem(row_idx, 4, QTableWidgetItem(row_data['number']))
            self.table.setItem(row_idx, 5, QTableWidgetItem(row_data['group_name']))
        
        self.stats_label.setText(f"Всего занятий: {len(rows)}")
    
    def _generate_schedule(self):
        generator = ScheduleGenerator()
        schedule, conflicts = generator.generate_schedule()
        generator.close()
        
        if conflicts:
            conflict_text = "\n".join(conflicts)
            QMessageBox.warning(self, "Предупреждение", f"Не удалось назначить все часы:\n{conflict_text}")
        
        self._load_schedule()
        QMessageBox.information(self, "Успех", f"Расписание составлено! Назначено занятий: {len(schedule)}")
    
    def _filter_schedule(self, day):
        self._load_schedule(day)
    
    def closeEvent(self, event):
        self.db.close()
        event.accept()