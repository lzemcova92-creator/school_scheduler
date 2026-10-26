from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTableWidget, 
                             QTableWidgetItem, QMessageBox, QComboBox)
from PyQt5.QtCore import Qt
from database.db_manager import DatabaseManager


class SubjectsWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.db = DatabaseManager()
        self.setWindowTitle("Управление предметами")
        self.resize(900, 600)
        self.setStyleSheet("background-color: #f0f2f5;")
        
        self._create_ui()
        self._load_subjects()
    
    def _create_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        title = QLabel("Предметы")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)
        
        input_layout = QHBoxLayout()
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Название предмета")
        input_layout.addWidget(self.name_input)
        
        self.teacher_combo = QComboBox()
        self.teacher_combo.addItem("Выберите преподавателя")
        self._load_teachers()
        input_layout.addWidget(self.teacher_combo)
        
        self.hours_input = QLineEdit()
        self.hours_input.setPlaceholderText("Часов в неделю")
        self.hours_input.setFixedWidth(150)
        input_layout.addWidget(self.hours_input)
        
        layout.addLayout(input_layout)
        
        btn_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("Добавить")
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #219a52;
            }
        """)
        self.add_btn.clicked.connect(self.add_subject)
        btn_layout.addWidget(self.add_btn)
        
        self.delete_btn = QPushButton("Удалить выбранный")
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
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.delete_btn.clicked.connect(self.delete_subject)
        btn_layout.addWidget(self.delete_btn)
        
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
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Преподаватель", "Часов/нед"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)
    
    def _load_teachers(self):
        teachers = self.db.execute_query("SELECT id, full_name FROM users WHERE role = 'teacher'")
        for teacher in teachers:
            self.teacher_combo.addItem(teacher['full_name'], teacher['id'])
    
    def _load_subjects(self):
        self.table.setRowCount(0)
        rows = self.db.execute_query("""
            SELECT s.id, s.name, u.full_name, s.hours_per_week 
            FROM subjects s 
            LEFT JOIN users u ON s.teacher_id = u.id
        """)
        
        for row_idx, row_data in enumerate(rows):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(row_data['id'])))
            self.table.setItem(row_idx, 1, QTableWidgetItem(row_data['name']))
            self.table.setItem(row_idx, 2, QTableWidgetItem(row_data['full_name'] or "Не назначен"))
            self.table.setItem(row_idx, 3, QTableWidgetItem(str(row_data['hours_per_week'])))
    
    def add_subject(self):
        name = self.name_input.text().strip()
        hours = self.hours_input.text().strip()
        
        if not name or not hours:
            QMessageBox.warning(self, "Ошибка", "Заполните название и часы!")
            return
        
        teacher_id = self.teacher_combo.currentData()
        
        try:
            hours_int = int(hours)
            self.db.execute_query(
                "INSERT INTO subjects (name, teacher_id, hours_per_week) VALUES (?, ?, ?)",
                (name, teacher_id, hours_int)
            )
            QMessageBox.information(self, "Успех", "Предмет добавлен!")
            self.name_input.clear()
            self.hours_input.clear()
            self._load_subjects()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить: {str(e)}")
    
    def delete_subject(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите предмет из таблицы!")
            return
        
        subject_id = self.table.item(selected_row, 0).text()
        subject_name = self.table.item(selected_row, 1).text()
        
        reply = QMessageBox.question(
            self, "Подтверждение",
            f"Вы действительно хотите удалить предмет {subject_name}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.db.execute_query("DELETE FROM subjects WHERE id = ?", (subject_id,))
            QMessageBox.information(self, "Успех", "Предмет удалён!")
            self._load_subjects()
    
    def closeEvent(self, event):
        self.db.close()
        event.accept()