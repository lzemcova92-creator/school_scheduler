from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QStackedWidget, QAction,
                             QMenuBar, QStatusBar, QMessageBox)
from PyQt5.QtCore import Qt
from ui.about_window import AboutWindow


class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle(f"Составитель расписания — {user['full_name']}")
        self.setMinimumSize(900, 600)
        self.setStyleSheet("background-color: #f0f2f5;")
        
        self._create_menu_bar()
        self._create_central_widget()
        self._create_status_bar()
    
    def _create_menu_bar(self):
        """Шапка (header) с меню — п.8"""
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #2c3e50;
                color: white;
                font-size: 14px;
            }
            QMenuBar::item:selected {
                background-color: #34495e;
            }
            QMenu {
                background-color: white;
                color: #333;
            }
            QMenu::item:selected {
                background-color: #4CAF50;
                color: white;
            }
        """)
        
        # Меню "Файл"
        file_menu = menubar.addMenu("Файл")
        file_menu.addAction("Выход", self.close)
        
        # Меню "Справочники"
        ref_menu = menubar.addMenu("Справочники")
        ref_menu.addAction("Преподаватели", lambda: self._show_message("Раздел в разработке"))
        ref_menu.addAction("Предметы", lambda: self._show_message("Раздел в разработке"))
        ref_menu.addAction("Аудитории", lambda: self._show_message("Раздел в разработке"))
        
        # Меню "Расписание"
        sched_menu = menubar.addMenu("Расписание")
        sched_menu.addAction("Просмотр", lambda: self._show_message("Раздел в разработке"))
        sched_menu.addAction("Составить автоматически", lambda: self._show_message("Раздел в разработке"))
        
        # Меню "Отчёты"
        rep_menu = menubar.addMenu("Отчёты")
        rep_menu.addAction("Экспорт в Excel", lambda: self._show_message("Раздел в разработке"))
        rep_menu.addAction("Экспорт в PDF", lambda: self._show_message("Раздел в разработке"))
        rep_menu.addAction("Резервная копия БД", lambda: self._show_message("Раздел в разработке"))
        
        # Меню "О программе"
        help_menu = menubar.addMenu("Справка")
        help_menu.addAction("О программе", self._open_about)
    
    def _create_central_widget(self):
        """Центральная часть с приветствием"""
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout(central)
        layout.setAlignment(Qt.AlignCenter)
        
        # Приветствие
        welcome = QLabel(f"Добро пожаловать, {self.user['full_name']}!")
        welcome.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #2c3e50;
            padding: 20px;
        """)
        welcome.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome)
        
        role_label = QLabel(f"Ваша роль: {self.user['role'].upper()}")
        role_label.setStyleSheet("font-size: 16px; color: #7f8c8d; padding: 10px;")
        role_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(role_label)
        
        layout.addSpacing(30)
        
        # Кнопки быстрого доступа
        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignCenter)
        
        btn_schedule = QPushButton("📅 Расписание")
        btn_teachers = QPushButton("‍🏫 Преподаватели")
        btn_classrooms = QPushButton("🏫 Аудитории")
        btn_reports = QPushButton(" Отчёты")
        
        for btn in [btn_schedule, btn_teachers, btn_classrooms, btn_reports]:
            btn.setFixedSize(180, 60)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-radius: 10px;
                    font-size: 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
                QPushButton:pressed {
                    background-color: #1f6391;
                }
            """)
            btn.clicked.connect(lambda: self._show_message("Раздел в разработке"))
            buttons_layout.addWidget(btn)
        
        layout.addLayout(buttons_layout)
    
    def _create_status_bar(self):
        """Подвал (footer) — п.8"""
        self.statusBar().showMessage(
            f"Пользователь: {self.user['username']} | Роль: {self.user['role']}"
        )
        self.statusBar().setStyleSheet("""
            QStatusBar {
                background-color: #2c3e50;
                color: white;
                font-size: 13px;
                padding: 5px;
            }
        """)
    
    def _open_about(self):
        """Открыть окно «О программе»"""
        self.about_window = AboutWindow()
        self.about_window.show()
    
    def _show_message(self, text):
        QMessageBox.information(self, "Информация", text)