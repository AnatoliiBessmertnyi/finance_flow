from PySide6 import QtWidgets
from PySide6.QtSql import QSqlTableModel
from src.operations.operations_controller import OperationsController
from src.operations.operations_handler import OperationsHandler

from src.main_window.main_window_handler import MainWindowHandler
from src.main_window.main_window_view import MainWindowView


class MainWindowController(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_window_view = MainWindowView()
        self.main_window_view.setupUi(self)
        self.main_window_handler = MainWindowHandler()
        self.main_window_handler.initialize_database()
        self.operations_handler = OperationsHandler(self.main_window_handler)

        self.load_operations()
        self.reload_data()

        self.main_window_view.new_btn.clicked.connect(
            self.open_new_operation_window
        )
        self.main_window_view.edit_btn.clicked.connect(
            self.open_edit_operation_window
        )
        self.main_window_view.delete_btn.clicked.connect(self.delete_operation)

    def load_operations(self):
        """Загружает операции из базы данных и отображает их в таблице."""
        operations = self.main_window_handler.fetch_all_operations()
        self.model = QSqlTableModel(self)
        self.model.setTable('finances')
        self.model.select()
        self.main_window_view.table_container.setModel(self.model)

    def reload_data(self):
        self.main_window_view.balance_lbl.setText(self.main_window_handler.total_balance())
        self.main_window_view.income_balance_lbl.setText(self.main_window_handler.total_income())
        self.main_window_view.outcome_balance_lbl.setText(self.main_window_handler.total_outcome())
        self.main_window_view.groceries_balance.setText(self.main_window_handler.total_groceries())
        self.main_window_view.marketplace_balance.setText(self.main_window_handler.total_marketplace())
        self.main_window_view.transport_balance.setText(self.main_window_handler.total_transport())
        self.main_window_view.entertainment_balance.setText(self.main_window_handler.total_entertainment())
        self.main_window_view.other_balance.setText(self.main_window_handler.total_other())

    def open_new_operation_window(self):
        """Открывает окно для добавления новой операции."""
        self.operations_controller = OperationsController(
            self, self.operations_handler, mode='new'
        )
        self.operations_controller.show()

    def open_edit_operation_window(self):
        """Открывает окно для редактирования выбранной операции."""
        selected_index = self.main_window_view.table_container.selectedIndexes()[0]
        operation_id = self.model.data(selected_index)
        self.operations_controller = OperationsController(
            self, self.operations_handler, mode='edit', operation_id=operation_id
        )
        self.operations_controller.show()

    def delete_operation(self):
        """Удаляет выбранную операцию."""
        selected_index = self.main_window_view.table_container.selectedIndexes()[0]
        operation_id = self.model.data(selected_index)
        self.operations_handler.delete_operation(operation_id)
        self.load_operations()
        self.reload_data()
