import sys
from PyQt5.QtWidgets import QApplication
from ui.login_window import LoginWindow
from utils.styles import load_styles

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Составитель расписания")
    
    # Применяем красивые стили
    load_styles(app)
    
    # Показываем окно входа
    login_window = LoginWindow()
    login_window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()