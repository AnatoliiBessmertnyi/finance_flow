from PySide6.QtWidgets import QDialog
from src.operations.operations_view import OperationsView
from src.operations.operations_handler import OperationsHandler


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
        self.view.setupUi(self)
        self.handler = handler
        self.mode = mode
        self.operation_id = operation_id

        if mode == 'edit':
            self.load_operation_data()

        self.view.pushButton.clicked.connect(self.save_operation)

    def load_operation_data(self):
        """Загружает данные операции для редактирования."""
        pass

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
