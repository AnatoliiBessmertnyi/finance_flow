import ctypes
import os

from PySide6 import QtWidgets
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow

from src.main_window.ui.main_window_ui import Ui_MainWindow


class MainWindowView(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def set_icon(self, app: QApplication) -> None:
        """Установка иконки

        :param QApplication app: Приложение
        """
        icon_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '../img',
            'main_icon.ico'
        )
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('myappid')
        app_icon = QIcon(icon_path)
        app.setWindowIcon(app_icon)
