from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from utils.auth import authenticate_user


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход в систему")
        self.setFixedSize(420, 380)
        self.setStyleSheet("background-color: #f0f2f5;")
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)
        layout.setContentsMargins(40, 30, 40, 30)
        
        title = QLabel("Составитель расписания")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Войдите в систему")
        subtitle.setStyleSheet("font-size: 14px; color: #7f8c8d;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(10)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Логин")
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
        """)
        layout.addWidget(self.username_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
        """)
        layout.addWidget(self.password_input)
        
        self.login_button = QPushButton("Войти")
        self.login_button.setFixedHeight(45)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        layout.addWidget(self.login_button)
        
        hint = QLabel("Тест: admin / admin123")
        hint.setStyleSheet("font-size: 12px; color: #95a5a6;")
        hint.setAlignment(Qt.AlignCenter)
        layout.addWidget(hint)
        
        self.login_button.clicked.connect(self.try_login)
        
        self._animate_appearance()
    
    def _animate_appearance(self):
        self.setWindowOpacity(0)
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.start()
    
    def try_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
            return
        
        user = authenticate_user(username, password)
        
        if user:
            QMessageBox.information(
                self, "Успех", 
                f"Добро пожаловать, {user['full_name']}!\nРоль: {user['role']}"
            )
            self.current_user = user
            self._open_main_window()
        else:
            QMessageBox.critical(self, "Ошибка", "Неверный логин или пароль!")
    
    def _open_main_window(self):
        from ui.main_window import MainWindow
        self.main_window = MainWindow(self.current_user)
        self.main_window.show()
        self.close()