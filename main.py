import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from src.main_window.ui.main_window_ui import Ui_MainWindow


class OperationTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OperationTracker()
    window.show()
    sys.exit(app.exec())
