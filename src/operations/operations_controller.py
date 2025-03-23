from typing import TYPE_CHECKING

from PySide6.QtCore import QDateTime
from PySide6.QtWidgets import QDialog

if TYPE_CHECKING:
    from src.operations.operations_handler import OperationsHandler
    from src.operations.operations_view import OperationsView


class OperationsController(QDialog):
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

        if mode == 'edit':
            self.load_operation_data()

        self.view.pushButton.clicked.connect(self.save_operation)

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
            self.view.operation_type_cb.setCurrentText(operation_data['status'])

    def save_operation(self):
        """Сохраняет новую или отредактированную операцию."""
        date = self.view.date.text()
        category = self.view.category_cb.currentText()
        description = self.view.description_le.text()
        balance = self.view.amount_le.text()
        status = self.view.operation_type_cb.currentText()
        if self.mode == 'new':
            self.handler.add_operation(
                date, category, description, balance, status
            )
        else:
            self.handler.edit_operation(
                self.operation_id, date, category, description, balance, status
            )

        self.accept()
