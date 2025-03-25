from typing import TYPE_CHECKING

from PySide6.QtSql import QSqlTableModel
from PySide6.QtWidgets import QMainWindow

from src.categories.categories_controller import CategoriesController
from src.categories.categories_handler import CategoriesHandler
from src.categories.categories_view import CategoriesView
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
        self.current_operations = []

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
        self.current_operations = self.handler.fetch_all_operations(
            self.current_period
        )
        self.model = QSqlTableModel(self)
        self.model.setTable('finances')

        date_filter = self.handler._get_date_filter(self.current_period)
        if date_filter:
            self.model.setFilter(date_filter)

        self.model.select()
        self.view.table_container.setModel(self.model)
        self.view.table_container.hideColumn(0)

    def show_category_statistics(self):
        """Выводит статистику по категориям на основе загруженных данных."""
        if not self.current_operations:
            print("Нет данных об операциях. Сначала загрузите операции.")
            return

        statistics = self.get_category_statistics()

        print("\nСтатистика по категориям (на основе загруженных операций):")
        print("----------------------------------------")
        for category, total in sorted(statistics.items(), key=lambda x: abs(x[1]), reverse=True):
            print(f"{category:<15}: {total:>8.2f}")
        print("----------------------------------------")

    def get_category_statistics(self):
        """
        Возвращает статистику по категориям на основе уже загруженных операций.
        Формат: {'Категория': сумма, ...}
        """
        statistics = {}

        for op in self.current_operations:
            category = op['category']
            amount = op['balance']
            statistics[category] = statistics.get(category, 0) + amount

        return statistics

    def get_category_shares_detailed(self, top_n=5):
        """
        Возвращает доли по категориям с правильным разделением на доходы и расходы.
        Для расходов берется абсолютное значение.
        Формат: {
            'income': {'Категория': доля_в_%, ...},
            'expense': {'Категория': доля_в_%, ...}
        }
        """
        if not self.current_operations:
            return {'income': {}, 'expense': {}}

        # Сначала правильно разделяем доходы и расходы
        income_stats = {}
        expense_stats = {}
        
        for op in self.current_operations:
            category = op['category']
            amount = op['balance']
            if amount >= 0:
                income_stats[category] = income_stats.get(category, 0) + amount
            else:
                expense_stats[category] = expense_stats.get(category, 0) + abs(amount)

        def calculate_shares(items, top_n):
            if not items:
                return {}
                
            total = sum(items.values())
            sorted_items = sorted(items.items(), key=lambda x: x[1], reverse=True)
            
            # Берем топ-N категорий или все, если их меньше
            top_items = sorted_items[:top_n]
            other_sum = sum(v for _, v in sorted_items[top_n:])
            
            shares = {
                k: (v / total) * 100
                for k, v in top_items
            }
            
            # Добавляем "Другое" только если есть что добавлять
            if other_sum > 0 and len(sorted_items) > top_n:
                shares['Остальное'] = (other_sum / total) * 100
                    
            return shares
        
        return {
            'income': calculate_shares(income_stats, top_n),
            'expense': calculate_shares(expense_stats, top_n)
        }

    def show_detailed_shares(self):
        """Выводит доли доходов и расходов с правильным разделением."""
        shares = self.get_category_shares_detailed()
        
        print("\nДетализация долей:")
        print("="*50)
        
        # Вывод доходов
        if shares['income']:
            print("\nДоходы (Топ-5 + Другое):")
            print("-"*50)
            for category, share in shares['income'].items():
                print(f"{category:<20}: {share:>6.2f}%")
            print(f"Всего категорий доходов: {len(shares['income'])}")
        else:
            print("\nНет данных о доходах")
        
        # Вывод расходов
        if shares['expense']:
            print("\nРасходы (Топ-5 + Другое):")
            print("-"*50)
            for category, share in shares['expense'].items():
                print(f"{category:<20}: {share:>6.2f}%")
            print(f"Всего категорий расходов: {len(shares['expense'])}")
        else:
            print("\nНет данных о расходах")
        
        print("="*50)

    def reload_data(self):
        self.view.balance_lbl.setText(
            self.handler.total_balance(self.current_period)
        )
        self.view.income_balance_lbl.setText(
            self.handler.total_income(self.current_period)
        )
        self.view.outcome_balance_lbl.setText(
            self.handler.total_outcome(self.current_period)
        )
        self.show_category_statistics()
        self.show_detailed_shares()

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
