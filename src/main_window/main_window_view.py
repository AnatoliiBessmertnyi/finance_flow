import ctypes
import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
                               QMainWindow, QMessageBox, QStyledItemDelegate,
                               QWidget, QFrame, QVBoxLayout)

from src.main_window.ui.main_window_ui import Ui_MainWindow


class MainWindowView(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.current_selected = 'income'

        self.income_frame.hide()
        self.setup_style()
        self.connect_signals()
        self.update_total_balance_styles()

    def connect_signals(self):
        self.income_widget.mousePressEvent = (
            lambda e: self.select_widget('income')
        )
        self.outcome_widget.mousePressEvent = (
            lambda e: self.select_widget('outcome')
        )

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
        self.active_style = ('''
            border: 1px solid rgba(255, 255, 255, 40);
            border-radius: 8px;
            background-color: rgba(255, 255, 255, 30);
        ''')
        self.inactive_style = ('''
            border: none;
            border-radius: none;
            background-color: none;
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

    def update_balances(self, sorted_data: dict) -> None:
        """Обновляет общие балансы.

        :param dict sorted_data: Отсортированные данные
        """
        total_income = sorted_data['income']['total']
        total_outcome = sorted_data['outcome']['total']
        self.balance_lbl.setText(str(int(total_income + total_outcome)))
        self.income_balance_lbl.setText(str(int(total_income)))
        self.outcome_balance_lbl.setText(str(int(total_outcome)))

    def select_widget(self, widget_type: str):
        self.current_selected = widget_type
        self.update_total_balance_styles()
        if widget_type == 'income':
            self.show_income_categories()
        else:
            self.show_outcome_categories()

    def update_total_balance_styles(self):
        self.income_widget.setStyleSheet(
            self.active_style
            if self.current_selected == 'income'
            else self.inactive_style
        )
        self.outcome_widget.setStyleSheet(
            self.active_style
            if self.current_selected == 'outcome'
            else self.inactive_style
        )

    def show_income_categories(self):
        self.outcome_frame.hide()
        self.income_frame.show()

    def show_outcome_categories(self):
        self.income_frame.hide()
        self.outcome_frame.show()

    def update_amount_category_widgets(
        self, sorted_data: dict, frame_type: str
    ) -> None:
        """Добавляет обновленные категории в outcome_frame.

        :param dict sorted_data: Отсортированные данные
        """
        frame = (
            self.income_frame
            if frame_type == 'income'
            else self.outcome_frame
        )
        self.clear_category_widgets(frame)
        categories_key = 'income' if frame_type == 'income' else 'outcome'
        categories = list(sorted_data[categories_key]['categories'].items())
        total_categories = len(categories)
        columns = 1 if total_categories <= 5 else 2

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(4)

        if columns == 1:
            v_layout = QVBoxLayout()
            v_layout.setSpacing(4)

            for name, data in categories:
                v_layout.addWidget(CategoryWidget(name, data['sum']))

            v_layout.addStretch()
            main_layout.addLayout(v_layout)
        else:
            v_layout1 = QVBoxLayout()
            v_layout1.setSpacing(4)
            v_layout2 = QVBoxLayout()
            v_layout2.setSpacing(4)
            half = (total_categories + 1) // 2

            for i, (name, data) in enumerate(categories):
                if i < half:
                    v_layout1.addWidget(CategoryWidget(name, data['sum']))
                else:
                    v_layout2.addWidget(CategoryWidget(name, data['sum']))

            v_layout1.addStretch()
            v_layout2.addStretch()

            h_layout = QHBoxLayout()
            h_layout.addLayout(v_layout1)
            h_layout.addLayout(v_layout2)
            h_layout.setSpacing(20)

            main_layout.addLayout(h_layout)

        if frame.layout():
            QWidget().setLayout(frame.layout())

        frame.setLayout(main_layout)

    def clear_category_widgets(self, frame: QFrame) -> None:
        """Очищает виджет категорий внутри outcome_frame."""
        if frame.layout() is None:
            return
        layout = frame.layout()

        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)

            if item.layout():
                for j in reversed(range(item.layout().count())):
                    child_item = item.layout().itemAt(j)
                    if child_item.widget() and isinstance(
                        child_item.widget(), CategoryWidget
                    ):
                        child_item.widget().deleteLater()
                item.layout().deleteLater()

            elif item.widget() and isinstance(item.widget(), CategoryWidget):
                item.widget().deleteLater()


class CenterAlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter


class CategoryWidget(QWidget):
    def __init__(self, name: str, amount: int, parent=None):
        super().__init__(parent)
        self.name = name
        self.amount = amount
        self.setup_ui()
        self.setup_style()

    def setup_ui(self):
        self.icon = QLabel()
        self.icon.setText('icon')
        self.icon.setFixedSize(24, 24)

        self.name_label = QLabel(self.name)
        self.name_label.setFixedSize(100, 24)
        self.name_label.setAlignment(Qt.AlignCenter)

        self.amount_label = QLabel(str(self.amount) + ' ₽')
        self.amount_label.setFixedSize(50, 24)

        container = QHBoxLayout()
        container.addWidget(self.icon)
        container.addWidget(self.name_label)
        container.addWidget(self.amount_label)

        self.setLayout(container)

    def setup_style(self):
        self.name_label.setStyleSheet('''
            background-color: rgba(255, 255, 255, 30);
            border: 1px solid  rgba(255, 255, 255, 40);
            border-radius: 4px;
            font: 500 13px "Roboto";
            color: #c8fafa;
        ''')
        self.amount_label.setStyleSheet('''
            background-color: rgba(255, 255, 255, 30);
            border: 1px solid  rgba(255, 255, 255, 40);
            border-radius: 4px;
            font: 600 14px "Roboto";
            color: #c8fafa;
        ''')
