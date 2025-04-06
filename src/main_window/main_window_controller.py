from typing import TYPE_CHECKING

from PySide6.QtSql import QSqlTableModel
from PySide6.QtWidgets import (QHBoxLayout, QMainWindow, QVBoxLayout,
                               QWidget)

from src.categories.categories_controller import CategoriesController
from src.categories.categories_handler import CategoriesHandler
from src.categories.categories_view import CategoriesView
from src.main_window.main_window_view import CategoryWidget
from src.operations.operations_controller import OperationsController
from src.operations.operations_handler import OperationsHandler
from src.operations.operations_view import OperationsView

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
        self.old_outcome_data = None
        self.old_income_data = None

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

        date_filter = self.handler.get_date_filter(self.current_period)
        if date_filter:
            self.model.setFilter(date_filter)

        self.model.select()
        self.view.table_container.setModel(self.model)
        self.view.table_container.hideColumn(0)

    def reload_data(self):
        sorted_data: dict = self.handler.get_category_statistics_detailed()
        self.view.update_balances(sorted_data)
        self.update_category_widgets(sorted_data)

    def update_category_widgets(self, sorted_data: dict) -> None:
        """Функция обновляет виджеты категорий если значения в них изменились.

        :param dict sorted_data: Сортированные данные
        """
        new_outcome_data = {
            'outcome': sorted_data['outcome']
        }
        new_income_data = {
            'income': sorted_data['income']
        }

        if new_outcome_data != self.old_outcome_data:
            self.view.update_amount_category_widgets(sorted_data, 'outcome')
        if new_income_data != self.old_income_data:
            self.view.update_amount_category_widgets(sorted_data, 'income')

        self.old_outcome_data = new_outcome_data
        self.old_income_data = new_income_data


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
            self.categories_view, self.categories_handler,
        )
        self.categories_controller.category_deleted.connect(
            self.handle_category_deleted
        )
        self.categories_controller.category_updated.connect(
            self.handle_category_updated
        )
        self.categories_view.exec()

    def handle_category_deleted(self, category_name: str) -> None:
        """Обработчик удаления категории"""
        operations_count = (
            self.operations_handler.get_operations_count_by_category(
                category_name
            )
        )

        if operations_count > 0:
            result = self.view.show_question(
                f'Категория "{category_name}" используется в '
                f'{operations_count} операциях. При удалении категории '
                'эти операции будут перемещены в категорию "Другое". '
                'Продолжить?'
            )
            if not result:
                return
            if not self.operations_handler.update_operations_category(
                category_name, 'Другое'
            ):
                self.view.show_message(
                    'Ошибка', 'Ошибка при обновлении операций.', 'error')
                return

        self.load_operations()
        self.reload_data()
        self.update_category_widgets(
            self.handler.get_category_statistics_detailed()
        )

    def handle_category_updated(self, old_name: str, new_name: str):
        """Обработчик изменения названия категории"""
        operations_count = (
            self.operations_handler.get_operations_count_by_category(old_name)
        )
        if operations_count > 0:
            if not self.operations_handler.update_operations_category(
                old_name, new_name
            ):
                self.view.show_error('Ошибка при обновлении операций.')
                self.restore_old_name()
                return

        self.load_operations()
        self.reload_data()
        self.update_category_widgets(
            self.handler.get_category_statistics_detailed()
        )
