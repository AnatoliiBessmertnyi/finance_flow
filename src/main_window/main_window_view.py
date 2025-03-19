from PySide6 import QtWidgets
from src.main_window.ui.main_window_ui import Ui_MainWindow


class MainWindowView(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
