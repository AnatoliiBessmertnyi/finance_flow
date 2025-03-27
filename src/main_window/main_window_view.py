import ctypes
import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QApplication, QHeaderView, QMainWindow,
                               QMessageBox, QStyledItemDelegate, QTableView)

from src.main_window.ui.main_window_ui import Ui_MainWindow


class MainWindowView(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup_style()

    def setup_style(self):
        self.table_container.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        delegate = CenterAlignDelegate(self.table_container)
        self.table_container.setItemDelegate(delegate)

        self.table_container.horizontalHeader().setStyleSheet('''
            QHeaderView::section {
                background-color: rgba(255, 255, 255, 40);
                border: 1px solid rgba(255, 255, 255, 50);
                color: #c8fafa;
                font: 600 14px "Roboto";
            }
        ''')
        self.table_container.setStyleSheet('''
            QTableView {
                background-color: rgba(255, 255, 255, 30);
                border: 1px solid  rgba(255, 255, 255, 40);
                border-bottom-left-radius: 6px;
                border-bottom-right-radius: 6px;
                font: 600 13px "Roboto";
                color: #185353;
                outline: none;
                selection-background-color: rgba(255, 255, 255, 40);
                selection-color: #c8fafa;
                show-decoration-selected: 1;
            }
            QTableView::item {
                border-bottom: 1px solid rgba(255, 255, 255, 50);
            }
        ''')

    def set_icon(self, app: QApplication) -> None:
        """Установка иконки.

        :param QApplication app: Приложение
        """
        icon_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '../img',
            'main_icon.ico'
        )
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            'myappid'
        )
        app_icon = QIcon(icon_path)
        app.setWindowIcon(app_icon)

    def show_message(
        self, title: str, message: str, message_type: str = 'info'
    ):
        """Показывает сообщение (ошибка, предупреждение, информация)."""
        if message_type == 'error':
            QMessageBox.critical(self, title, message)
        elif message_type == 'warning':
            QMessageBox.warning(self, title, message)
        elif message_type == 'info':
            QMessageBox.information(self, title, message)


class CenterAlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter
