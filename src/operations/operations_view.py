from PySide6.QtWidgets import QDialog
from PySide6.QtGui import QIcon

from src.operations.ui.new_operation_ui import Ui_Dialog


class OperationsView(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.set_style()

    def set_locales(self, mode: str) -> None:
        if mode == 'new':
            title_text = 'Новая операция'
            btn_text = 'Добавить операцию'
        else:
            title_text = 'Редактировать операцию'
            btn_text = 'Сохранить изменения'
        self.title_lbl.setText(title_text)
        self.ok_btn.setText(btn_text)

    def set_style(self):
        self.ok_btn.setIcon(QIcon('src/img/done.svg'))
