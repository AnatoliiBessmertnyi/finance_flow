from datetime import datetime, timedelta

from PySide6 import QtSql, QtWidgets


class MainWindowHandler:
    DEFAULT_CATEGORIES = [
        'Продукты',
        'Транспорт',
        'Жилье',
        'Развлечения',
        'Другое'
    ]

    def __init__(self):
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('finance_db.db')

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
        date_filter = self._get_date_filter(period)
        sql_query = f'SELECT * FROM finances WHERE {date_filter}'
        print(sql_query)
        query = self.execute_query(sql_query)
        print(query)
        operations = []
        while query.next():
            operations.append({
                'id': query.value('ID'),
                'date': query.value('Date'),
                'category': query.value('Category'),
                'description': query.value('Description'),
                'balance': query.value('Balance')
            })
        print(operations)
        return operations

    def get_total(self, column, condition=None, period='month'):
        """Возвращает сумму значений в колонке с опциональным условием."""
        date_filter = self._get_date_filter(period)
        sql_query = f'SELECT SUM({column}) FROM finances'

        conditions = []
        if date_filter:
            conditions.append(date_filter)
        if condition:
            conditions.append(condition)
        if conditions:
            sql_query += ' WHERE ' + ' AND '.join(conditions)

        query = self.execute_query(sql_query)
        if query.next():
            return str(query.value(0)) or '0'
        return '0'

    def total_balance(self, period='month'):
        return self.get_total(column='Balance', period=period)

    def total_income(self, period='month'):
        return self.get_total(
            column='Balance', condition='Balance >= 0', period=period
        )

    def total_outcome(self, period='month'):
        return self.get_total(
            column='Balance', condition='Balance < 0', period=period
        )

    def _get_date_filter(self, period='month'):
        today = datetime.now()

        if period == 'day':
            date_str = today.strftime('%Y-%m-%d')
            return f'Date LIKE "{date_str}%"'

        elif period == 'week':
            start_date = today - timedelta(days=today.weekday())
            end_date = start_date + timedelta(days=6)
            start_str = start_date.strftime('%Y-%m-%d 00:00')
            end_str = end_date.strftime('%Y-%m-%d 23:59')
            return f'Date BETWEEN "{start_str}" AND "{end_str}"'

        elif period == 'month':
            first_day = today.replace(day=1)
            next_month = first_day.replace(day=28) + timedelta(days=4)
            last_day = next_month - timedelta(days=next_month.day)
            start_str = first_day.strftime('%Y-%m-%d 00:00')
            end_str = last_day.strftime('%Y-%m-%d 23:59')
            return f'Date BETWEEN "{start_str}" AND "{end_str}"'

        elif period == 'year':
            first_day = today.replace(month=1, day=1)
            last_day = today.replace(month=12, day=31)
            start_str = first_day.strftime('%Y-%m-%d 00:00')
            end_str = last_day.strftime('%Y-%m-%d 23:59')
            return f'Date BETWEEN "{start_str}" AND "{end_str}"'

        else:
            return '1=1'
