import ctypes
import math
import os

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QBrush, QColor, QFont, QIcon, QPainter, QPen, QPixmap
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
                               QLabel, QMainWindow, QMessageBox,
                               QStyledItemDelegate, QVBoxLayout, QWidget)

from src.main_window.ui.main_window_ui import Ui_MainWindow


class MainWindowView(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.current_selected = 'outcome'

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
            QWidget {
                border: 2px solid rgba(255, 255, 255, 35);
                border-radius: 8px;
                background-color: rgba(255, 255, 255, 25);
            }
        ''')
        self.inactive_style = ('''
            QWidget {
                border: none;
                border-radius: 8px;
                background-color: none;
            }
            QWidget:hover {
                border: 1px solid rgba(255, 255, 255, 20);
                background-color: rgba(255, 255, 255, 10);
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

    def update_balances(self, sorted_data: dict) -> None:
        """Обновляет общие балансы.

        :param dict sorted_data: Отсортированные данные
        """
        total_income = sorted_data['income']['total']
        total_outcome = sorted_data['outcome']['total']
        self.balance_lbl.setText(str(int(total_income + total_outcome)) + ' ₽')
        self.income_balance_lbl.setText(str(int(total_income)) + ' ₽')
        self.outcome_balance_lbl.setText(str(int(total_outcome)) + ' ₽')

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
        categories_dict = sorted_data[categories_key]['categories']
        categories_list = list(categories_dict.items())
        total_categories = len(categories_list)
        columns = 1 if total_categories <= 5 else 2

        if columns == 1:
            main_layout = QHBoxLayout()

            pie_chart = PieChartWidget(categories_dict)
            pie_chart.setStyleSheet("background: transparent;")
            main_layout.addWidget(pie_chart)

            v_layout = QVBoxLayout()
            v_layout.setSpacing(4)
            for name, data in categories_list:
                v_layout.addWidget(CategoryWidget(name, data['sum']))
            v_layout.addStretch()

            main_layout.addLayout(v_layout)
        else:
            main_layout = QVBoxLayout()
            v_layout1 = QVBoxLayout()
            v_layout1.setSpacing(4)
            v_layout2 = QVBoxLayout()
            v_layout2.setSpacing(4)
            half = (total_categories + 1) // 2

            for i, (name, data) in enumerate(categories_list):
                if i < half:
                    v_layout1.addWidget(CategoryWidget(name, data['sum']))
                else:
                    v_layout2.addWidget(CategoryWidget(name, data['sum']))

            v_layout1.addStretch()
            v_layout2.addStretch()

            h_layout = QHBoxLayout()
            h_layout.addLayout(v_layout1)
            h_layout.addLayout(v_layout2)
            h_layout.setSpacing(4)

            main_layout.addLayout(h_layout)

        if frame.layout():
            QWidget().setLayout(frame.layout())

        frame.setLayout(main_layout)

    def clear_category_widgets(self, frame: QFrame) -> None:
        """Очистка фрейма."""
        if frame.layout():
            old_layout = frame.layout()
            temp_widget = QWidget()
            temp_widget.setLayout(old_layout)
            temp_widget.deleteLater()
        frame.setLayout(QVBoxLayout())


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
        self.name_label.setMinimumSize(100, 24)
        self.name_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.amount_label = QLabel(str(int(self.amount)) + ' ₽')
        self.amount_label.setMinimumSize(80, 24)
        self.amount_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        container = QHBoxLayout()
        container.addWidget(self.icon)
        container.addWidget(self.name_label)
        container.addWidget(self.amount_label)

        self.setLayout(container)

    def setup_style(self):
        self.name_label.setStyleSheet('''
            background-color: rgba(255, 255, 255, 20);
            border: 1px solid  rgba(255, 255, 255, 30);
            border-radius: 4px;
            font: 500 13px "Roboto";
            color: #c8fafa;
            padding-left: 4px;
        ''')
        self.amount_label.setStyleSheet('''
            background-color: rgba(255, 255, 255, 20);
            border: 1px solid  rgba(255, 255, 255, 30);
            border-radius: 4px;
            font: 600 14px "Roboto";
            color: #c8fafa;
            padding-right: 4px;
        ''')


class PieChartWidget(QWidget):
    def __init__(self, categories_data, parent=None):
        super().__init__(parent)
        self.categories = categories_data
        self.total_amount = sum(data['sum'] for data in categories_data.values())
        self.setMinimumSize(200, 200)

        layout = QVBoxLayout()
        layout.addWidget(
            PieChartDrawingWidget(categories_data, self.total_amount)
        )
        self.setLayout(layout)


class PieChartDrawingWidget(QWidget):
    MIN_SEGMENT_ANGLE = 9

    def __init__(self, categories_data, total_amount, parent=None):
        super().__init__(parent)
        self.categories = categories_data
        self.total_amount = total_amount
        self.setMaximumSize(200, 200)
        self.colors = [
            QColor(100, 200, 200),
            QColor(200, 150, 100),
            QColor(150, 200, 150),
            QColor(200, 100, 150),
            QColor(150, 150, 200),
            QColor(200, 200, 100),
            QColor(100, 150, 200),
            QColor(200, 100, 100),
        ]

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        size = min(self.width(), self.height()) - 40
        rect = QRectF(
            (self.width() - size) / 2,
            (self.height() - size) / 2,
            size, size
        )
        # Сначала вычисляем общее количество "маленьких" сегментов
        sorted_categories = sorted(
            self.categories.items(),
            key=lambda item: item[1]['sum'],
            reverse=True
        )
        # Вычисляем сколько градусов займут все минимальные сегменты
        small_segments_count = sum(
            1 for _, data in sorted_categories
            if data['sum'] / self.total_amount < 0.03
        )
        total_min_angles = small_segments_count * self.MIN_SEGMENT_ANGLE
        # Вычисляем сколько градусов останется для нормальных сегментов
        remaining_angle = 360 - total_min_angles
        remaining_total = sum(
            data['sum'] for _, data in sorted_categories
            if data['sum'] / self.total_amount >= 0.03
        )

        start_angle = 0
        color_index = 0

        sorted_categories = sorted(
            self.categories.items(),
            key=lambda item: item[1]['sum'],
            reverse=True
        )

        for _, data in sorted_categories:
            percentage = data['sum'] / self.total_amount
            if percentage < 0.03:
                span_angle = self.MIN_SEGMENT_ANGLE
            else:
                span_angle = (data['sum'] / remaining_total) * remaining_angle

            color = self.colors[color_index % len(self.colors)]
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(Qt.black, 1))
            painter.drawPie(rect, int(start_angle * 16), int(span_angle * 16))

            middle_angle = start_angle + span_angle / 2
            radian = math.radians(middle_angle)
            label_radius = size / 2 + 15
            x = rect.center().x() + label_radius * math.cos(radian)
            y = rect.center().y() + label_radius * math.sin(radian)

            label = f'{percentage:.1%}'
            painter.setPen(QPen(Qt.white))
            font = QFont('Roboto', 8)
            font.setBold(True)
            painter.setFont(font)

            text_rect = painter.boundingRect(QRectF(), Qt.AlignCenter, label)
            text_rect.moveCenter(QPointF(x, y))
            painter.drawText(text_rect, Qt.AlignCenter, label)

            start_angle += span_angle
            color_index += 1

        center_size = size / 1.5
        center_rect = QRectF(
            rect.center().x() - center_size/2,
            rect.center().y() - center_size/2,
            center_size, center_size
        )
        painter.setBrush(QBrush(QColor(50, 70, 70)))
        painter.drawEllipse(center_rect)

        font = QFont('Roboto', 10)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(QPen(Qt.white))
        painter.drawText(
            center_rect,
            Qt.AlignCenter,
            f'{int(self.total_amount)} ₽'
        )
