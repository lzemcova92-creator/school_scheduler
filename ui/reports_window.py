from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from reports.report_generator import ReportGenerator


class ReportsWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.report_gen = ReportGenerator()
        self.setWindowTitle("Отчёты")
        self.resize(600, 400)
        self.setStyleSheet("background-color: #f0f2f5;")
        
        self._create_ui()
    
    def _create_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        title = QLabel("Отчёты и резервное копирование")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        layout.addSpacing(30)
        
        # Кнопки
        btn_excel = QPushButton("Экспорт расписания в Excel")
        btn_excel.setFixedHeight(50)
        btn_excel.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #219a52;
            }
        """)
        btn_excel.clicked.connect(self._export_excel)
        layout.addWidget(btn_excel)
        
        btn_pdf = QPushButton("Экспорт расписания в PDF")
        btn_pdf.setFixedHeight(50)
        btn_pdf.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        btn_pdf.clicked.connect(self._export_pdf)
        layout.addWidget(btn_pdf)
        
        btn_backup = QPushButton("Резервная копия базы данных")
        btn_backup.setFixedHeight(50)
        btn_backup.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        btn_backup.clicked.connect(self._backup_db)
        layout.addWidget(btn_backup)
        
        layout.addStretch()
        
        # Кнопка назад
        btn_back = QPushButton("Назад")
        btn_back.setFixedHeight(40)
        btn_back.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        btn_back.clicked.connect(self.close)
        layout.addWidget(btn_back)
    
    def _export_excel(self):
        try:
            filepath = self.report_gen.export_to_excel()
            QMessageBox.information(self, "Успех", f"Отчёт сохранён:\n{filepath}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать отчёт:\n{str(e)}")
    
    def _export_pdf(self):
        try:
            filepath = self.report_gen.export_to_pdf()
            QMessageBox.information(self, "Успех", f"Отчёт сохранён:\n{filepath}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать отчёт:\n{str(e)}")
    
    def _backup_db(self):
        try:
            filepath = self.report_gen.backup_database()
            QMessageBox.information(self, "Успех", f"Резервная копия создана:\n{filepath}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать резервную копию:\n{str(e)}")
    
    def closeEvent(self, event):
        self.report_gen.close()
        event.accept()