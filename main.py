import sys

from PySide6.QtWidgets import QApplication

from src.main_window.main_window_controller import MainWindowController
from src.main_window.main_window_handler import MainWindowHandler
from src.main_window.main_window_view import MainWindowView

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = MainWindowView()
    view.set_icon(app)
    handler = MainWindowHandler()
    controller = MainWindowController(view, handler)
    view.show()
    sys.exit(app.exec())
