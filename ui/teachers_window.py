from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTableWidget, 
                             QTableWidgetItem, QMessageBox)
from PyQt5.QtCore import Qt
from database.db_manager import DatabaseManager
import bcrypt


class TeachersWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.db = DatabaseManager()
        self.setWindowTitle("Управление преподавателями")
        self.resize(900, 600)
        self.setStyleSheet("background-color: #f0f2f5;")
        
        self._create_ui()
        self._load_teachers()
    
    def _create_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Заголовок
        title = QLabel("Преподаватели")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)
        
        # Поля ввода
        input_layout = QHBoxLayout()
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("ФИО преподавателя")
        input_layout.addWidget(self.name_input)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Логин")
        input_layout.addWidget(self.username_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        input_layout.addWidget(self.password_input)
        
        layout.addLayout(input_layout)
        
        # Кнопки
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
        self.add_btn.clicked.connect(self.add_teacher)
        btn_layout.addWidget(self.add_btn)
        
        self.delete_btn = QPushButton("Удалить выбранного")
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
        self.delete_btn.clicked.connect(self.delete_teacher)
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
        
        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Логин", "ФИО", "Роль"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)
    
    def _load_teachers(self):
        self.table.setRowCount(0)
        rows = self.db.execute_query("SELECT id, username, full_name, role FROM users WHERE role = 'teacher'")
        
        for row_idx, row_data in enumerate(rows):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(row_data['id'])))
            self.table.setItem(row_idx, 1, QTableWidgetItem(row_data['username']))
            self.table.setItem(row_idx, 2, QTableWidgetItem(row_data['full_name']))
            self.table.setItem(row_idx, 3, QTableWidgetItem(row_data['role']))
    
    def add_teacher(self):
        name = self.name_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not name or not username or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
            return
        
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        try:
            self.db.execute_query(
                "INSERT INTO users (username, password_hash, full_name, role) VALUES (?, ?, ?, ?)",
                (username, password_hash, name, 'teacher')
            )
            QMessageBox.information(self, "Успех", "Преподаватель добавлен!")
            self.name_input.clear()
            self.username_input.clear()
            self.password_input.clear()
            self._load_teachers()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить: {str(e)}")
    
    def delete_teacher(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите преподавателя из таблицы!")
            return
        
        teacher_id = self.table.item(selected_row, 0).text()
        teacher_name = self.table.item(selected_row, 2).text()
        
        reply = QMessageBox.question(
            self, "Подтверждение",
            f"Вы действительно хотите удалить преподавателя {teacher_name}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.db.execute_query("DELETE FROM users WHERE id = ?", (teacher_id,))
            QMessageBox.information(self, "Успех", "Преподаватель удалён!")
            self._load_teachers()
    
    def closeEvent(self, event):
        self.db.close()
        event.accept()