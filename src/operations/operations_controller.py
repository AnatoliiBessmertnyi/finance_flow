from typing import TYPE_CHECKING

from PySide6.QtCore import QDateTime, Signal
from PySide6.QtWidgets import QDialog

if TYPE_CHECKING:
    from src.operations.operations_handler import OperationsHandler
    from src.operations.operations_view import OperationsView


class OperationsController(QDialog):
    last_category = Signal(str)

    def __init__(
        self,
        view: 'OperationsView',
        handler: 'OperationsHandler',
        mode: str = 'new',
        operation_id: int = None
    ):
        super().__init__()
        self.view = view
        self.handler = handler
        self.mode = mode
        self.operation_id = operation_id
        self.current_categories = []

        self.load_categories()
        if self.mode == 'new':
            self.view.date.setDateTime(QDateTime.currentDateTime())
        else:
            self.load_operation_data()

        self.view.set_locales(self.mode)
        self.connect_signals()

    def connect_signals(self) -> None:
        """Подключает сигналы."""
        self.view.ok_btn.clicked.connect(self.save_operation)

    def load_categories(self):
        """Загружает категории из базы данных и добавляет их в QComboBox."""
        new_categories = self.handler.get_all_categories()
        if new_categories != self.current_categories:
            self.current_categories = new_categories
            self.view.category_cb.clear()
            self.view.category_cb.addItems(new_categories)

    def load_operation_data(self):
        """Загружает данные операции для редактирования."""
        operation_data = self.handler.get_operation_by_id(self.operation_id)
        if operation_data:
            date_time = QDateTime.fromString(
                operation_data['date'], 'dd.MM.yyyy HH:mm'
            )
            self.view.date.setDateTime(date_time)
            self.view.category_cb.setCurrentText(operation_data['category'])
            self.view.description_le.setText(operation_data['description'])
            self.view.amount_le.setText(str(operation_data['balance']))

    def save_operation(self):
        """Сохраняет новую или отредактированную операцию."""
        if not self.validate_form():
            return
        date = self.view.date.text()
        category = self.view.category_cb.currentText()
        description = self.view.description_le.text()
        balance = self.view.amount_le.text()
        if self.mode == 'new':
            self.handler.add_operation(date, category, description, balance)
        else:
            self.handler.edit_operation(
                self.operation_id, date, category, description, balance
            )
        self.last_category.emit(category)

        self.view.accept()

    def validate_form(self) -> bool:
        """Проверяет, что форма заполнена корректно."""
        if not self.view.category_cb.currentText():
            self.view.show_message(
                "Ошибка",
                "Выберите категорию",
                "error"
            )
            return False
        elif not self.view.amount_le.text():
            self.view.show_message(
                "Ошибка",
                "Введите сумму",
                "error"
            )
            return False
        else:
            return True
