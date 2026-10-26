from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter, QColor, QLinearGradient


class AnimatedBackground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.angle = 0
        
        # Таймер для анимации
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(50)  # Обновление каждые 50 мс
        
        self.setMinimumSize(100, 100)
    
    def update_animation(self):
        self.angle = (self.angle + 1) % 360
        self.update()  # Перерисовка
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Создаём градиент
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        
        # Цвета меняются в зависимости от угла
        r1 = int(128 + 50 * __import__('math').sin(__import__('math').radians(self.angle)))
        g1 = int(200 + 30 * __import__('math').cos(__import__('math').radians(self.angle * 0.7)))
        b1 = int(220 + 20 * __import__('math').sin(__import__('math').radians(self.angle * 1.3)))
        
        r2 = int(200 + 30 * __import__('math').cos(__import__('math').radians(self.angle * 0.5)))
        g2 = int(220 + 20 * __import__('math').sin(__import__('math').radians(self.angle * 0.8)))
        b2 = int(240 + 15 * __import__('math').cos(__import__('math').radians(self.angle * 1.1)))
        
        gradient.setColorAt(0, QColor(r1, g1, b1, 80))
        gradient.setColorAt(1, QColor(r2, g2, b2, 80))
        
        painter.fillRect(self.rect(), gradient)
        painter.end()