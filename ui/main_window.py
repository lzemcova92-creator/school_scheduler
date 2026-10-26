import math
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QLinearGradient
from ui.about_window import AboutWindow
from ui.teachers_window import TeachersWindow
from ui.classrooms_window import ClassroomsWindow
from ui.subjects_window import SubjectsWindow
from ui.schedule_window import ScheduleWindow


class AnimatedBackground(QWidget):
    """Анимированный фон главного окна (требование п.4)"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.angle = 0
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(50)
        
        self.setMinimumSize(100, 100)
    
    def update_animation(self):
        self.angle = (self.angle + 1) % 360
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        
        r1 = int(128 + 50 * math.sin(math.radians(self.angle)))
        g1 = int(200 + 30 * math.cos(math.radians(self.angle * 0.7)))
        b1 = int(220 + 20 * math.sin(math.radians(self.angle * 1.3)))
        
        r2 = int(200 + 30 * math.cos(math.radians(self.angle * 0.5)))
        g2 = int(220 + 20 * math.sin(math.radians(self.angle * 0.8)))
        b2 = int(240 + 15 * math.cos(math.radians(self.angle * 1.1)))
        
        gradient.setColorAt(0, QColor(r1, g1, b1, 60))
        gradient.setColorAt(1, QColor(r2, g2, b2, 60))
        
        painter.fillRect(self.rect(), gradient)
        painter.end()


class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle(f"Составитель расписания — {user['full_name']}")
        self.resize(1000, 700)
        
        # Создаём меню и статус-бар
        self._create_menu_bar()
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Анимированный фон
        self.background = AnimatedBackground(central_widget)
        self.background.setGeometry(0, 0, self.width(), self.height())
        self.background.lower()
        
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
            background-color: rgba(255, 255, 255, 180);
            border-radius: 10px;
        """)
        welcome.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(welcome)
        
        # Роль
        role_label = QLabel(f"Ваша роль: {self.user['role'].upper()}")
        role_label.setStyleSheet("""
            font-size: 18px;
            color: #7f8c8d;
            padding: 10px;
            background-color: rgba(255, 255, 255, 180);
            border-radius: 10px;
        """)
        role_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(role_label)
        
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
        
        # Общий стиль для кнопок
        button_style = """
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
        
        # Применяем стили и подключаем обработчики
        btn_schedule.setStyleSheet(button_style)
        btn_schedule.setFixedSize(200, 70)
        btn_schedule.clicked.connect(self._open_schedule)
        
        btn_teachers.setStyleSheet(button_style)
        btn_teachers.setFixedSize(200, 70)
        btn_teachers.clicked.connect(self._open_teachers)
        
        btn_classrooms.setStyleSheet(button_style)
        btn_classrooms.setFixedSize(200, 70)
        btn_classrooms.clicked.connect(self._open_classrooms)
        
        btn_reports.setStyleSheet(button_style)
        btn_reports.setFixedSize(200, 70)
        btn_reports.clicked.connect(lambda: self._show_message("Раздел Отчёты в разработке"))
        
        # Добавляем кнопки в layout
        buttons_layout.addWidget(btn_schedule)
        buttons_layout.addWidget(btn_teachers)
        buttons_layout.addWidget(btn_classrooms)
        buttons_layout.addWidget(btn_reports)
        
        main_layout.addLayout(buttons_layout)
        main_layout.addStretch()
        
        # Статус-бар
        self._create_status_bar()
    
    def resizeEvent(self, event):
        """Обновляем размер фона при изменении размера окна"""
        if hasattr(self, 'background'):
            self.background.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)
    
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
        ref_menu.addAction("Предметы", self._open_subjects)
        ref_menu.addAction("Аудитории", self._open_classrooms)
        
        sched_menu = menubar.addMenu("Расписание")
        sched_menu.addAction("Просмотр расписания", self._open_schedule)
        sched_menu.addAction("Составить автоматически", self._open_schedule)
        
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
    
    def _open_classrooms(self):
        self.classrooms_window = ClassroomsWindow(self.user)
        self.classrooms_window.show()
    
    def _open_subjects(self):
        self.subjects_window = SubjectsWindow(self.user)
        self.subjects_window.show()
    
    def _open_schedule(self):
        self.schedule_window = ScheduleWindow(self.user)
        self.schedule_window.show()
    
    def _show_message(self, text):
        QMessageBox.information(self, "Информация", text)