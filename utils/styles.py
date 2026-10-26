def load_styles(app):
    """Глобальные стили приложения"""
    style_sheet = """
    QMainWindow {
        background-color: #f0f2f5;
    }
    QPushButton {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 6px;
        font-size: 14px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
    QPushButton:pressed {
        background-color: #3d8b40;
    }
    QLineEdit {
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 6px;
        font-size: 14px;
        background-color: white;
    }
    QLineEdit:focus {
        border: 2px solid #4CAF50;
    }
    QLabel {
        font-size: 16px;
        color: #333;
    }
    """
    app.setStyleSheet(style_sheet)