from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QIcon, QRegularExpressionValidator
from PySide6.QtWidgets import QDialog, QMessageBox

from src.operations.ui.new_operation_ui import Ui_Dialog


class OperationsView(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.set_style()

    def set_locales(self, mode: str) -> None:
        """Устанавливает текст.

        :param str mode: Режим создания или редактирования
        """
        if mode == 'new':
            title_text = 'Новая операция'
            btn_text = 'Добавить операцию'
        else:
            title_text = 'Редактировать операцию'
            btn_text = 'Сохранить изменения'
        self.title_lbl.setText(title_text)
        self.ok_btn.setText(btn_text)

    def set_style(self) -> None:
        """Устанавливает стили."""
        self.category_cb.setStyleSheet('''
            QComboBox {
                border: 1px solid rgba(255, 255, 255, 40);
                border-radius: 6px;
                color: #c8fafa;
                background: rgba(255, 255, 255, 30);
                font: 14px "Roboto";
                padding-left: 10px;
            }
            QComboBox::drop-down {
                border-radius: 4px;
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
            }
            QComboBox:hover {
                background: rgba(255, 255, 255, 40);
                border: 1px solid rgba(255, 255, 255, 50);
            }
            QComboBox::down-arrow {
                image: url(src/img/arrow_left.svg);
                width: 20px;
                height: 20px;
            }
            QComboBox::down-arrow:hover {
                image: url(src/img/arrow_down.svg);
                width: 20px;
                height: 20px;
            }
            QComboBox::down-arrow:on {
                image: url(src/img/arrow_down.svg);
                width: 20px;
                height: 20px;
            }
            QAbstractItemView {
                border: 1px solid #1890FF;
                border-radius: 4px;
                background: #1EACD1;
                color: #c8fafa;
                outline: none;
            }
            QAbstractItemView::item {
                border: none;
                height: 21px;
                padding-left: 7px;
            }
            QAbstractItemView::item:hover {
                background: #1890FF;
                color: #c8fafa;
            }
            QAbstractItemView::item:selected {
                background-color: #1890FF;
                color: #c8fafa;
            }
        ''')

        self.ok_btn.setIcon(QIcon('src/img/done.svg'))

        pattern = QRegularExpression(r'^\d*([.,]?\d{0,2})?$')
        validator = QRegularExpressionValidator(pattern)
        self.amount_le.setValidator(validator)

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
