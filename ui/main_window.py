from ui.classrooms_window import ClassroomsWindow
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from ui.about_window import AboutWindow
from ui.teachers_window import TeachersWindow


class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle(f"Составитель расписания — {user['full_name']}")
        self.resize(1000, 700)
        self.setStyleSheet("background-color: #f0f2f5;")
        
        # Создаём центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной вертикальный layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(50, 50, 50, 50)
        
        # Заголовок
        welcome = QLabel(f"Добро пожаловать, {self.user['full_name']}!")
        welcome.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #2c3e50;
            padding: 20px;
        """)
        welcome.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(welcome)
        
        # Роль
        role_label = QLabel(f"Ваша роль: {self.user['role'].upper()}")
        role_label.setStyleSheet("font-size: 18px; color: #7f8c8d; padding: 10px;")
        role_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(role_label)
        
        # Пустое пространство
        main_layout.addSpacing(40)
        
        # Горизонтальный layout для кнопок
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(30)
        buttons_layout.setAlignment(Qt.AlignCenter)
        
        # Создаём кнопки
        btn_schedule = QPushButton("Расписание")
        btn_teachers = QPushButton("Преподаватели")
        btn_classrooms = QPushButton("Аудитории")
        btn_reports = QPushButton("Отчёты")
        
        # Стиль для синих кнопок
        blue_style = """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 18px;
                font-weight: bold;
                padding: 15px 30px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1f6391;
            }
        """
        
        # Стиль для зелёной кнопки
        green_style = """
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 18px;
                font-weight: bold;
                padding: 15px 30px;
            }
            QPushButton:hover {
                background-color: #219a52;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """
        
        # Применяем стили и подключаем обработчики
        btn_schedule.setStyleSheet(blue_style)
        btn_schedule.setFixedSize(200, 70)
        btn_schedule.clicked.connect(lambda: self._show_message("Раздел Расписание в разработке"))
        
        btn_teachers.setStyleSheet(green_style)
        btn_teachers.setFixedSize(200, 70)
        btn_teachers.clicked.connect(self._open_teachers)
        
        btn_classrooms.setStyleSheet(blue_style)
        btn_classrooms.setFixedSize(200, 70)
        btn_classrooms.clicked.connect(self._open_classrooms)
        
        btn_reports.setStyleSheet(blue_style)
        btn_reports.setFixedSize(200, 70)
        btn_reports.clicked.connect(lambda: self._show_message("Раздел Отчёты в разработке"))
        
        # Добавляем кнопки в горизонтальный layout
        buttons_layout.addWidget(btn_schedule)
        buttons_layout.addWidget(btn_teachers)
        buttons_layout.addWidget(btn_classrooms)
        buttons_layout.addWidget(btn_reports)
        
        # Добавляем горизонтальный layout в основной
        main_layout.addLayout(buttons_layout)
        
        # Растягиваем нижнюю часть
        main_layout.addStretch()
        
        # Создаём меню и статус-бар
        self._create_menu_bar()
        self._create_status_bar()
    
    def _create_menu_bar(self):
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
        
        file_menu = menubar.addMenu("Файл")
        file_menu.addAction("Выход", self.close)
        
        ref_menu = menubar.addMenu("Справочники")
        ref_menu.addAction("Преподаватели", self._open_teachers)
        ref_menu.addAction("Предметы", lambda: self._show_message("Раздел в разработке"))
        ref_menu.addAction("Аудитории", lambda: self._show_message("Раздел в разработке"))
        
        sched_menu = menubar.addMenu("Расписание")
        sched_menu.addAction("Просмотр", lambda: self._show_message("Раздел в разработке"))
        sched_menu.addAction("Составить автоматически", lambda: self._show_message("Раздел в разработке"))
        
        rep_menu = menubar.addMenu("Отчёты")
        rep_menu.addAction("Экспорт в Excel", lambda: self._show_message("Раздел в разработке"))
        rep_menu.addAction("Экспорт в PDF", lambda: self._show_message("Раздел в разработке"))
        rep_menu.addAction("Резервная копия БД", lambda: self._show_message("Раздел в разработке"))
        
        help_menu = menubar.addMenu("Справка")
        help_menu.addAction("О программе", self._open_about)
    
    def _create_status_bar(self):
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
        self.about_window = AboutWindow()
        self.about_window.show()
    
    def _open_teachers(self):
        self.teachers_window = TeachersWindow(self.user)
        self.teachers_window.show()
    
    def _show_message(self, text):
        QMessageBox.information(self, "Информация", text)

    def _open_classrooms(self):
        self.classrooms_window = ClassroomsWindow(self.user)
        self.classrooms_window.show()