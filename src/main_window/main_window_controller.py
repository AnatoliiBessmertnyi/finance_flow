from PySide6.QtSql import QSqlTableModel
from PySide6.QtWidgets import QMainWindow

from src.main_window.main_window_handler import MainWindowHandler
from src.main_window.main_window_view import MainWindowView
from src.operations.operations_controller import OperationsController
from src.operations.operations_handler import OperationsHandler
from src.operations.operations_view import OperationsView


class MainWindowController(QMainWindow):
    def __init__(self, view: 'MainWindowView', handler: 'MainWindowHandler'):
        super().__init__()
        self.view = view
        self.handler = handler
        self.handler.initialize_database()

        self.load_operations()
        self.reload_data()

        self.view.new_btn.clicked.connect(self.open_new_operation_window)
        self.view.edit_btn.clicked.connect(self.open_edit_operation_window)
        self.view.delete_btn.clicked.connect(self.delete_operation)

    def load_operations(self):
        """Загружает операции из базы данных и отображает их в таблице."""
        self.handler.fetch_all_operations()
        self.model = QSqlTableModel(self)
        self.model.setTable('finances')
        self.model.select()
        self.view.table_container.setModel(self.model)

    def reload_data(self):
        self.view.balance_lbl.setText(self.handler.total_balance())
        self.view.income_balance_lbl.setText(self.handler.total_income())
        self.view.outcome_balance_lbl.setText(self.handler.total_outcome())
        self.view.groceries_balance.setText(self.handler.total_groceries())
        self.view.marketplace_balance.setText(self.handler.total_marketplace())
        self.view.transport_balance.setText(self.handler.total_transport())
        self.view.entertainment_balance.setText(
            self.handler.total_entertainment()
        )
        self.view.other_balance.setText(self.handler.total_other())

    def open_new_operation_window(self):
        """Открывает окно для добавления новой операции."""
        print(self.sender())
        self.operations_view = OperationsView()
        self.operations_handler = OperationsHandler(self.handler)
        self.operations_controller = OperationsController(
            self.operations_view, self.operations_handler, mode='new'
        )
        self.operations_controller.exec()
        self.load_operations()
        self.reload_data()

    def open_edit_operation_window(self):
        """Открывает окно для редактирования выбранной операции."""
        selected_index = self.view.table_container.selectedIndexes()[0]
        operation_id = self.model.data(selected_index)
        print(self.sender())

        self.operations_view = OperationsView()
        self.operations_handler = OperationsHandler(self.handler)
        self.operations_controller = OperationsController(
            self.operations_view,
            self.operations_handler,
            mode='edit',
            operation_id=operation_id
        )
        self.operations_controller.exec()
        self.load_operations()
        self.reload_data()

    def delete_operation(self):
        """Удаляет выбранную операцию."""
        selected_index = self.view.table_container.selectedIndexes()[0]
        operation_id = self.model.data(selected_index)
        self.new_operation_handler.delete_operation(operation_id)
        self.load_operations()
        self.reload_data()
