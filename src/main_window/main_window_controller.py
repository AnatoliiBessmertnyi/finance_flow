from typing import TYPE_CHECKING

from PySide6.QtSql import QSqlTableModel
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget

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
        self.current_selected = 'outcome'

        self.initialize_operations()
        self.load_operations()
        self.reload_data()
        self.setup_widget_selection()

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

    def setup_widget_selection(self):
        self.view.income_widget.mousePressEvent = (
            lambda e: self.select_widget('income')
        )
        self.view.outcome_widget.mousePressEvent = (
            lambda e: self.select_widget('outcome')
        )

        self.update_widget_styles()

    def select_widget(self, widget_type):
        self.current_selected = widget_type
        self.update_widget_styles()

        if widget_type == 'income':
            self.show_income()
        else:
            self.show_outcome()

    def update_widget_styles(self):
        self.view.income_widget.setStyleSheet(
            self.view.active_style
            if self.current_selected == 'income'
            else self.view.inactive_style
        )
        self.view.outcome_widget.setStyleSheet(
            self.view.active_style
            if self.current_selected == 'outcome'
            else self.view.inactive_style
        )

    def show_income(self):
        self.view.outcome_frame.hide()
        self.view.income_frame.show()

    def show_outcome(self):
        self.view.income_frame.hide()
        self.view.outcome_frame.show()

    def reload_data(self):
        sorted_data: dict = self.handler.get_category_statistics_detailed()
        total_income = sorted_data['income']['total']
        total_outcome = sorted_data['expense']['total']
        self.view.balance_lbl.setText(str(int(total_income + total_outcome)))
        self.view.income_balance_lbl.setText(str(int(total_income)))
        self.view.outcome_balance_lbl.setText(str(int(total_outcome)))
        self.update_amount_category_widgets(sorted_data)

    def clear_category_widgets(self) -> None:
        """Очищает виджет категорий внутри outcome_frame."""
        if self.view.outcome_frame.layout() is None:
            return

        layout = self.view.outcome_frame.layout()

        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)

            if item.layout():
                for j in reversed(range(item.layout().count())):
                    child_item = item.layout().itemAt(j)
                    if child_item.widget() and isinstance(child_item.widget(), CategoryWidget):
                        child_item.widget().deleteLater()
                item.layout().deleteLater()

            elif item.widget() and isinstance(item.widget(), CategoryWidget):
                item.widget().deleteLater()

    def update_amount_category_widgets(self, sorted_data: dict) -> None:
        """Добавляет обновленные категории в outcome_frame.

        :param dict sorted_data: Отсортированные данные
        """
        self.clear_category_widgets()

        categories = list(sorted_data['expense']['categories'].items())
        total_categories = len(categories)
        columns = 1 if total_categories <= 5 else 2

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(10)

        if columns == 1:
            v_layout = QVBoxLayout()
            v_layout.setSpacing(5)

            for name, data in categories:
                v_layout.addWidget(CategoryWidget(name, data['sum']))

            v_layout.addStretch()
            main_layout.addLayout(v_layout)
        else:
            v_layout1 = QVBoxLayout()
            v_layout1.setSpacing(5)
            v_layout2 = QVBoxLayout()
            v_layout2.setSpacing(5)
            half = (total_categories + 1) // 2

            for i, (name, data) in enumerate(categories):
                if i < half:
                    v_layout1.addWidget(CategoryWidget(name, data['sum']))
                else:
                    v_layout2.addWidget(CategoryWidget(name, data['sum']))

            v_layout1.addStretch()
            v_layout2.addStretch()

            h_layout = QHBoxLayout()
            h_layout.addLayout(v_layout1)
            h_layout.addLayout(v_layout2)
            h_layout.setSpacing(20)

            main_layout.addLayout(h_layout)

        if self.view.outcome_frame.layout():
            QWidget().setLayout(self.view.outcome_frame.layout())

        self.view.outcome_frame.setLayout(main_layout)

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
