from datetime import datetime, timedelta

from PySide6 import QtSql, QtWidgets


class MainWindowHandler:
    DEFAULT_CATEGORIES = [
        'Жилье',
        'Продукты',
        'Развлечения',
        'Транспорт',
        'Другое'
    ]

    def __init__(self):
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('finance_db.db')
        self.operations = []

    def initialize_database(self):
        """Создает базу данных и таблицы, если они не существуют."""
        if not self.db.open():
            QtWidgets.QMessageBox.critical(
                None,
                'Ошибка базы данных',
                'Не удалось открыть базу данных.',
                QtWidgets.QMessageBox.Cancel
            )
            return False

        query = QtSql.QSqlQuery()
        query.exec('''
            CREATE TABLE IF NOT EXISTS finances (
                ID integer primary key AUTOINCREMENT,
                Date VARCHAR(20),
                Category VARCHAR(20),
                Description VARCHAR(20),
                Balance REAL
            )
        ''')

        query.exec('''
            CREATE TABLE IF NOT EXISTS categories (
                ID integer primary key AUTOINCREMENT,
                Name VARCHAR(20) UNIQUE
            )
        ''')
        self._initialize_default_categories()

        return True

    def _initialize_default_categories(self):
        """Инициализирует базовые категории при первом запуске."""
        query = QtSql.QSqlQuery(self.db)
        query.exec('SELECT COUNT(*) FROM categories')
        if query.next() and query.value(0) == 0:
            for category in self.DEFAULT_CATEGORIES:
                query.prepare('INSERT INTO categories (Name) VALUES (?)')
                query.addBindValue(category)
                query.exec()

    def execute_query(self, sql_query, params=None):
        """Выполняет SQL-запрос с параметрами."""
        query = QtSql.QSqlQuery(self.db)
        query.prepare(sql_query)

        if params:
            for value in params:
                query.addBindValue(value)

        if not query.exec():
            print('Ошибка выполнения запроса:', query.lastError().text())
        return query

    def fetch_all_operations(self, period='month'):
        """Возвращает все операции из базы данных."""
        operations = []
        date_filter = self.get_date_filter(period)
        sql_query = f'SELECT * FROM finances WHERE {date_filter}'
        query = self.execute_query(sql_query)
        while query.next():
            operations.append({
                'id': query.value('ID'),
                'date': query.value('Date'),
                'category': query.value('Category'),
                'description': query.value('Description'),
                'balance': query.value('Balance')
            })
        self.operations = operations

    def get_category_statistics_detailed(self, top_n=7):
        """
        Возвращает статистику по категориям с разделением на доходы/расходы.
        Вызывается из контроллера с уже загруженными операциями.
        """
        if not self.operations:
            return {
                'income': {'total': 0, 'categories': {}},
                'outcome': {'total': 0, 'categories': {}}
            }

        income_stats = {}
        outcome_stats = {}
        total_income = 0
        total_outcome = 0

        for op in self.operations:
            category = op['category']
            amount = op['balance']
            if amount >= 0:
                income_stats[category] = income_stats.get(category, 0) + amount
                total_income += amount
            else:
                outcome_stats[category] = (
                    outcome_stats.get(category, 0) + amount
                )
                total_outcome += amount

        def calculate_shares(items, total_amount, top_n):
            if not items or total_amount == 0:
                return {}

            if total_amount < 0:
                sorted_items = sorted(
                    items.items(), key=lambda x: abs(x[1]), reverse=True
                )
                total_amount = abs(total_amount)
            else:
                sorted_items = sorted(
                    items.items(), key=lambda x: x[1], reverse=True
                )

            top_items = sorted_items[:top_n]
            other_sum = sum(v for _, v in sorted_items[top_n:])

            result = {}
            for category, amount in top_items:
                result[category] = {
                    'sum': amount,
                    'share': (abs(amount) / total_amount) * 100
                }

            if other_sum != 0 and len(sorted_items) > top_n:
                result['Остальное'] = {
                    'sum': other_sum,
                    'share': (abs(other_sum) / total_amount) * 100
                }

            return result

        return {
            'income': {
                'total': total_income,
                'categories': calculate_shares(
                    income_stats, total_income, top_n
                )
            },
            'outcome': {
                'total': total_outcome,
                'categories': calculate_shares(
                    outcome_stats, total_outcome, top_n
                )
            }
        }

    def get_date_filter(self, period='current_month', start_day: int = 1):
        today = datetime.now()

        if period == 'current_month':
            if today.day >= start_day:
                start_date = today.replace(day=start_day)
                end_date = (
                    start_date + timedelta(days=32)
                ).replace(day=start_day) - timedelta(days=1)
            else:
                end_date = today.replace(day=start_day) - timedelta(days=1)
                start_date = (
                    end_date - timedelta(days=32)
                ).replace(day=start_day)
            return self.get_date_range_filter(start_date, end_date)

        elif period == 'previous_month':
            if today.day >= start_day:
                end_date = today.replace(day=start_day) - timedelta(days=1)
                start_date = (
                    end_date - timedelta(days=32)
                ).replace(day=start_day)
            else:
                start_date = (
                    today.replace(day=start_day) - timedelta(days=32)
                ).replace(day=start_day)
                end_date = today.replace(day=start_day) - timedelta(days=1)
            return self.get_date_range_filter(start_date, end_date)

        elif period == 'current_year':
            if today.day >= start_day:
                start_date = today.replace(month=1, day=start_day)
                try:
                    end_date = today.replace(
                        month=12, day=start_day-1
                    ) + timedelta(days=1)
                except ValueError:
                    end_date = today.replace(month=12, day=31)
            else:
                start_date = today.replace(
                    year=today.year-1, month=1, day=start_day
                )
                try:
                    end_date = today.replace(day=start_day) - timedelta(days=1)
                except ValueError:
                    end_date = today.replace(day=1) - timedelta(days=1)
            return self.get_date_range_filter(start_date, end_date)

        else:
            return '1=1'

    def get_date_range_filter(self, start_date: int, end_date: int):
        """Формирует SQL-условие для диапазона дат"""
        start_str = start_date.strftime('%Y-%m-%d 00:00')
        end_str = end_date.strftime('%Y-%m-%d 23:59')
        return f"Date BETWEEN '{start_str}' AND '{end_str}'"
