from PySide6 import QtWidgets
from src.operations.operations_view import OperationsView


class OperationsController(QtWidgets.QDialog):
    def __init__(
        self, parent, operations_handler, mode='new', operation_id=None
    ):
        super().__init__(parent)
        self.ui = OperationsView()
        self.ui.setupUi(self)
        self.operations_handler = operations_handler
        self.mode = mode
        self.operation_id = operation_id

        if mode == 'edit':
            self.load_operation_data()

        self.ui.pushButton.clicked.connect(self.save_operation)

    def load_operation_data(self):
        """Загружает данные операции для редактирования."""
        # Здесь можно добавить логику загрузки данных операции по ID
        pass

    def save_operation(self):
        """Сохраняет новую или отредактированную операцию."""
        date = self.ui.date.text()
        category = self.ui.category_cb.currentText()
        description = self.ui.description_le.text()
        balance = self.ui.amount_le.text()
        status = self.ui.operation_type_cb.currentText()
        print(self.mode)
        print(self.sender())
        if self.mode == 'new':
            self.operations_handler.add_operation(
                date, category, description, balance, status
            )
        else:
            self.operations_handler.edit_operation(
                self.operation_id, date, category, description, balance, status
            )

        self.parent().load_operations()
        self.parent().reload_data()
        self.close()
