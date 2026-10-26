from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton)
from PyQt5.QtCore import Qt


class AboutWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("О программе")
        self.setFixedSize(450, 350)
        self.setStyleSheet("background-color: #f0f2f5;")
        
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout(central)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)
        
        title = QLabel("Составитель расписания")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        layout.addWidget(QLabel("Версия: 1.0"))
        
        # ЗАМЕНИ НА СВОИ ДАННЫЕ!
        fio = QLabel("Выполнил: Иванов Иван Иванович")
        fio.setStyleSheet("font-size: 14px; font-weight: bold; color: #34495e;")
        fio.setAlignment(Qt.AlignCenter)
        layout.addWidget(fio)
        
        group = QLabel("Группа: ИС-201")
        group.setStyleSheet("font-size: 14px; color: #7f8c8d;")
        group.setAlignment(Qt.AlignCenter)
        layout.addWidget(group)
        
        layout.addSpacing(20)
        
        desc = QLabel("Приложение для автоматического\nсоставления школьного расписания")
        desc.setAlignment(Qt.AlignCenter)
        desc.setStyleSheet("font-size: 13px; color: #95a5a6;")
        layout.addWidget(desc)
        
        layout.addSpacing(20)
        
        close_btn = QPushButton("Закрыть")
        close_btn.setFixedWidth(150)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn, alignment=Qt.AlignCenter)