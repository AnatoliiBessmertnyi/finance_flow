import sys
from PySide6.QtWidgets import QApplication
from src.main_window.main_window_controller import MainWindowController

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindowController()
    window.show()
    sys.exit(app.exec())
