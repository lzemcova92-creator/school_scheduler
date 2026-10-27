from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTableWidget, 
                             QTableWidgetItem, QMessageBox, QComboBox, QCheckBox)
from PyQt5.QtCore import Qt
from database.db_manager import DatabaseManager
import bcrypt


class UsersWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.db = DatabaseManager()
        self.setWindowTitle("Управление пользователями")
        self.resize(1000, 600)
        self.setStyleSheet("background-color: #f0f2f5;")
        
        self._create_ui()
        self._load_users()
    
    def _create_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        title = QLabel("Управление пользователями")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)
        
        # Поля ввода
        input_layout = QHBoxLayout()
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Логин")
        input_layout.addWidget(self.username_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        input_layout.addWidget(self.password_input)
        
        self.fullname_input = QLineEdit()
        self.fullname_input.setPlaceholderText("ФИО преподавателя")
        input_layout.addWidget(self.fullname_input)
        
        self.role_combo = QComboBox()
        self.role_combo.addItems(["teacher", "admin"])
        input_layout.addWidget(self.role_combo)
        
        layout.addLayout(input_layout)
        
        # Чекбоксы прав
        rights_layout = QHBoxLayout()
        
        self.can_edit_checkbox = QCheckBox("Может редактировать расписание")
        self.can_edit_checkbox.setChecked(True)
        rights_layout.addWidget(self.can_edit_checkbox)
        
        self.can_manage_checkbox = QCheckBox("Может управлять пользователями")
        rights_layout.addWidget(self.can_manage_checkbox)
        
        layout.addLayout(rights_layout)
        
        # Кнопки
        btn_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("Добавить пользователя")
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
            QPushButton:hover { background-color: #219a52; }
        """)
        self.add_btn.clicked.connect(self.add_user)
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
            QPushButton:hover { background-color: #c0392b; }
        """)
        self.delete_btn.clicked.connect(self.delete_user)
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
            QPushButton:hover { background-color: #7f8c8d; }
        """)
        self.back_btn.clicked.connect(self.close)
        btn_layout.addWidget(self.back_btn)
        
        layout.addLayout(btn_layout)
        
        # Таблица пользователей
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Логин", "ФИО", "Роль", "Редактирует", "Управляет"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)
    
    def _load_users(self):
        self.table.setRowCount(0)
        rows = self.db.execute_query("SELECT id, username, full_name, role, can_edit_schedule, can_manage_users FROM users ORDER BY id")
        
        for row_idx, row_data in enumerate(rows):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(row_data['id'])))
            self.table.setItem(row_idx, 1, QTableWidgetItem(row_data['username']))
            self.table.setItem(row_idx, 2, QTableWidgetItem(row_data['full_name']))
            self.table.setItem(row_idx, 3, QTableWidgetItem(row_data['role']))
            self.table.setItem(row_idx, 4, QTableWidgetItem("Да" if row_data['can_edit_schedule'] else "Нет"))
            self.table.setItem(row_idx, 5, QTableWidgetItem("Да" if row_data['can_manage_users'] else "Нет"))
    
    def add_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        fullname = self.fullname_input.text().strip()
        role = self.role_combo.currentText()
        can_edit = self.can_edit_checkbox.isChecked()
        can_manage = self.can_manage_checkbox.isChecked()
        
        if not username or not password or not fullname:
            QMessageBox.warning(self, "Ошибка", "Заполните все обязательные поля!")
            return
        
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        try:
            self.db.execute_query(
                """INSERT INTO users (username, password_hash, full_name, role, can_edit_schedule, can_manage_users) 
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (username, password_hash, fullname, role, can_edit, can_manage)
            )
            QMessageBox.information(self, "Успех", f"Пользователь {fullname} добавлен!")
            self.username_input.clear()
            self.password_input.clear()
            self.fullname_input.clear()
            self._load_users()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить: {str(e)}")
    
    def delete_user(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя из таблицы!")
            return
        
        user_id = self.table.item(selected_row, 0).text()
        user_name = self.table.item(selected_row, 2).text()
        
        if user_id == str(self.user['id']):
            QMessageBox.warning(self, "Ошибка", "Нельзя удалить самого себя!")
            return
        
        reply = QMessageBox.question(
            self, "Подтверждение",
            f"Вы действительно хотите удалить пользователя {user_name}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.db.execute_query("DELETE FROM users WHERE id = %s", (user_id,))
            QMessageBox.information(self, "Успех", "Пользователь удалён!")
            self._load_users()
    
    def closeEvent(self, event):
        self.db.close()
        event.accept()