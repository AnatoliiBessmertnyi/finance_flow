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
                Balance REAL
            )
        ''')
        query.exec('''
            CREATE TABLE IF NOT EXISTS categories (
                ID integer primary key AUTOINCREMENT,
                Name VARCHAR(20)
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
                'balance': query.value('Balance')
            })
        return operations

    def get_total(self, column, condition=None):
        """Возвращает сумму значений в колонке с опциональным условием."""
        sql_query = f'SELECT SUM({column}) FROM finances'
        if condition:
            sql_query += f' WHERE {condition}'

        query = self.execute_query(sql_query)
        if query.next():
            return str(query.value(0)) or '0'
        return '0'

    def total_balance(self):
        return self.get_total(column='Balance')

    def total_income(self):
        return self.get_total(column='Balance', condition='Balance >= 0')

    def total_outcome(self):
        return self.get_total(column='Balance', condition='Balance < 0')
