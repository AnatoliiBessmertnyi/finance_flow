from PySide6 import QtSql, QtWidgets


class MainWindowHandler:
    def __init__(self):
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('finance_db.db')

    def initialize_database(self):
        """Создает базу данных и таблицы, если они не существуют."""
        if not self.db.open():
            QtWidgets.QMessageBox.critical(
                None,
                "Ошибка базы данных",
                "Не удалось открыть базу данных.",
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
                Balance REAL,
                Status VARCHAR(20)
            )
        ''')
        return True

    def execute_query(self, sql_query, params=None):
        """Выполняет SQL-запрос с параметрами."""
        query = QtSql.QSqlQuery(self.db)
        query.prepare(sql_query)

        if params:
            for value in params:
                query.addBindValue(value)

        if not query.exec():
            print("Ошибка выполнения запроса:", query.lastError().text())
        return query

    def fetch_all_operations(self):
        """Возвращает все операции из базы данных."""
        query = self.execute_query('SELECT * FROM finances')
        operations = []
        while query.next():
            operations.append({
                'id': query.value('ID'),
                'date': query.value('Date'),
                'category': query.value('Category'),
                'description': query.value('Description'),
                'balance': query.value('Balance'),
                'status': query.value('Status')
            })
        return operations

    def get_total(self, column, filter=None, value=None):
        """Возвращает сумму значений в колонке с опциональным фильтром."""
        sql_query = f'SELECT SUM({column}) FROM finances'
        if filter and value:
            sql_query += f' WHERE {filter} = ?'
            params = [value]
        else:
            params = None

        query = self.execute_query(sql_query, params)
        if query.next():
            return str(query.value(0)) or '0'
        return '0'

    def total_balance(self):
        return self.get_total(column='Balance')

    def total_income(self):
        return self.get_total(column='Balance', filter='Status', value='Доход')

    def total_outcome(self):
        return self.get_total(column='Balance', filter='Status', value='Затраты')

    def total_groceries(self):
        return self.get_total(column='Balance', filter='Category', value='Продукты')

    def total_marketplace(self):
        return self.get_total(column='Balance', filter='Category', value='Маркетплейсы')

    def total_transport(self):
        return self.get_total(column='Balance', filter='Category', value='Транспорт')

    def total_entertainment(self):
        return self.get_total(column='Balance', filter='Category', value='Развлечения')

    def total_other(self):
        return self.get_total(column='Balance', filter='Category', value='Другое')