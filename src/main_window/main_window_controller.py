from typing import TYPE_CHECKING

from PySide6.QtSql import QSqlTableModel
from PySide6.QtWidgets import QMainWindow, QVBoxLayout

from src.categories.categories_controller import CategoriesController
from src.categories.categories_handler import CategoriesHandler
from src.categories.categories_view import CategoriesView
from src.operations.operations_controller import OperationsController
from src.operations.operations_handler import OperationsHandler
from src.operations.operations_view import OperationsView
from src.main_window.main_window_view import CategoryWidget

if TYPE_CHECKING:
    from src.main_window.main_window_handler import MainWindowHandler
    from src.main_window.main_window_view import MainWindowView


class MainWindowController(QMainWindow):
    def __init__(self, view: 'MainWindowView', handler: 'MainWindowHandler'):
        super().__init__()
        self.view = view
        self.handler = handler
        self.handler.initialize_database()
        self.current_period = 'month'

        self.initialize_operations()
        self.load_operations()
        self.reload_data()

        self.view.new_btn.clicked.connect(self.open_operation_window)
        self.view.edit_btn.clicked.connect(self.open_operation_window)
        self.view.delete_btn.clicked.connect(self.delete_operation)
        self.view.category_edit_btn.clicked.connect(self.open_categories)

    def initialize_operations(self):
        self.operations_view = OperationsView()
        self.operations_handler = OperationsHandler(self.handler)

    def load_operations(self):
        """Загружает операции из базы данных и отображает их в таблице."""
        self.handler.fetch_all_operations(self.current_period)
        self.model = QSqlTableModel(self)
        self.model.setTable('finances')

        date_filter = self.handler._get_date_filter(self.current_period)
        if date_filter:
            self.model.setFilter(date_filter)

        self.model.select()
        self.view.table_container.setModel(self.model)
        self.view.table_container.hideColumn(0)

    def reload_data(self):
        sorted_data: dict = self.handler.get_category_statistics_detailed()
        total_income = sorted_data['income']['total']
        total_outcome = sorted_data['expense']['total']
        self.view.balance_lbl.setText(str(int(total_income + total_outcome)))
        self.view.income_balance_lbl.setText(str(int(total_income)))
        self.view.outcome_balance_lbl.setText(str(int(total_outcome)))
        self.update_amount_category(sorted_data)

    def update_amount_category(self, sorted_data: dict) -> None:
        self.clear_category_widgets()
        self.update_amount_category_widgets(sorted_data)

    def clear_category_widgets(self) -> None:
        """Очищает виджет категорий."""
        category_widgets_count = 0

        for i in reversed(range(self.view.category_container.count())):
            item = self.view.category_container.itemAt(i)

            if item.layout():
                for j in reversed(range(item.layout().count())):
                    child_item = item.layout().itemAt(j)
                    if child_item.widget() and isinstance(
                        child_item.widget(), CategoryWidget
                    ):
                        category_widgets_count += 1
                        child_item.widget().deleteLater()
                item.layout().deleteLater()

            elif item.widget() and isinstance(item.widget(), CategoryWidget):
                category_widgets_count += 1
                item.widget().deleteLater()

    def update_amount_category_widgets(self, sorted_data: dict) -> None:
        """Добавляет обновленные категории.

        :param dict sorted_data: Данные по категориям
        """
        categories = list(sorted_data['expense']['categories'].items())
        total_categories = len(categories)
        columns = 1 if total_categories <= 5 else 2

        if columns == 1:
            v_layout = QVBoxLayout()
            v_layout.setSpacing(5)

            for name, data in categories:
                v_layout.addWidget(CategoryWidget(name, data['sum']))

            v_layout.addStretch()
            self.view.category_container.addLayout(v_layout)

        else:
            v_layout_1 = QVBoxLayout()
            v_layout_1.setSpacing(5)
            v_layout_2 = QVBoxLayout()
            v_layout_2.setSpacing(5)
            half = (total_categories + 1) // 2

            for i, (name, data) in enumerate(categories):
                if i < half:
                    v_layout_1.addWidget(CategoryWidget(name, data['sum']))
                else:
                    v_layout_2.addWidget(CategoryWidget(name, data['sum']))

            v_layout_1.addStretch()
            v_layout_2.addStretch()
            self.view.category_container.addLayout(v_layout_1)
            self.view.category_container.addLayout(v_layout_2)

    def open_operation_window(self):
        """Открывает окно для добавления новой операции."""
        operation_id = None
        sender = self.sender()
        mode = 'new' if sender.objectName() == 'new_btn' else 'edit'

        if mode == 'edit':
            selected_index = self.view.table_container.selectedIndexes()
            if not selected_index:
                self.view.show_message(
                    'Ошибка',
                    'Выберите операцию для редактирования.',
                    'error'
                )
                return
            selected_row = selected_index[0].row()
            operation_id = self.model.data(self.model.index(selected_row, 0))

        self.operations_controller = OperationsController(
            self.operations_view, self.operations_handler, mode, operation_id
        )
        self.operations_view.exec()
        self.load_operations()
        self.reload_data()

    def delete_operation(self):
        """Удаляет выбранную операцию."""
        selected_index = self.view.table_container.selectedIndexes()
        if not selected_index:
            self.view.show_message(
                'Ошибка',
                'Выберите операцию для удаления.',
                'error'
            )
            return
        selected_row = selected_index[0].row()
        operation_id = self.model.data(self.model.index(selected_row, 0))
        self.operations_handler.delete_operation(operation_id)
        self.load_operations()
        self.reload_data()

    def open_categories(self):
        self.categories_view = CategoriesView()
        self.categories_handler = CategoriesHandler(self.handler)
        self.categories_controller = CategoriesController(
            self.categories_view, self.categories_handler
        )
        self.categories_view.exec()
