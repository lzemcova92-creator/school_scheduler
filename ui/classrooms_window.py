from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTableWidget, 
                             QTableWidgetItem, QMessageBox)
from PyQt5.QtCore import Qt
from database.db_manager import DatabaseManager


class ClassroomsWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.db = DatabaseManager()
        self.setWindowTitle("Управление аудиториями")
        self.resize(900, 600)
        self.setStyleSheet("background-color: #f0f2f5;")
        
        self._create_ui()
        self._load_classrooms()
    
    def _create_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        title = QLabel("Аудитории")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)
        
        input_layout = QHBoxLayout()
        
        self.number_input = QLineEdit()
        self.number_input.setPlaceholderText("Номер аудитории")
        input_layout.addWidget(self.number_input)
        
        self.capacity_input = QLineEdit()
        self.capacity_input.setPlaceholderText("Вместимость")
        input_layout.addWidget(self.capacity_input)
        
        self.equipment_input = QLineEdit()
        self.equipment_input.setPlaceholderText("Оборудование")
        input_layout.addWidget(self.equipment_input)
        
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
        self.add_btn.clicked.connect(self.add_classroom)
        btn_layout.addWidget(self.add_btn)
        
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
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.delete_btn.clicked.connect(self.delete_classroom)
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
        self.table.setHorizontalHeaderLabels(["ID", "Номер", "Вместимость", "Оборудование"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)
    
    def _load_classrooms(self):
        self.table.setRowCount(0)
        rows = self.db.execute_query("SELECT id, number, capacity, equipment FROM classrooms")
        
        for row_idx, row_data in enumerate(rows):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(row_data['id'])))
            self.table.setItem(row_idx, 1, QTableWidgetItem(row_data['number']))
            self.table.setItem(row_idx, 2, QTableWidgetItem(str(row_data['capacity'])))
            self.table.setItem(row_idx, 3, QTableWidgetItem(row_data['equipment'] or ""))
    
    def add_classroom(self):
        number = self.number_input.text().strip()
        capacity = self.capacity_input.text().strip()
        equipment = self.equipment_input.text().strip()
        
        if not number or not capacity:
            QMessageBox.warning(self, "Ошибка", "Заполните номер и вместимость!")
            return
        
        try:
            capacity_int = int(capacity)
            self.db.execute_query(
                "INSERT INTO classrooms (number, capacity, equipment) VALUES (?, ?, ?)",
                (number, capacity_int, equipment)
            )
            QMessageBox.information(self, "Успех", "Аудитория добавлена!")
            self.number_input.clear()
            self.capacity_input.clear()
            self.equipment_input.clear()
            self._load_classrooms()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить: {str(e)}")
    
    def delete_classroom(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите аудиторию из таблицы!")
            return
        
        classroom_id = self.table.item(selected_row, 0).text()
        classroom_number = self.table.item(selected_row, 1).text()
        
        reply = QMessageBox.question(
            self, "Подтверждение",
            f"Вы действительно хотите удалить аудиторию {classroom_number}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.db.execute_query("DELETE FROM classrooms WHERE id = ?", (classroom_id,))
            QMessageBox.information(self, "Успех", "Аудитория удалена!")
            self._load_classrooms()
    
    def closeEvent(self, event):
        self.db.close()
        event.accept()