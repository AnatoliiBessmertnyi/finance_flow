from PySide6 import QtWidgets, QtSql


class Data:
    def __init__(self):
        super().__init__()
        self.create_connection()

    def create_connection(self):
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('finance_db.db')

        if not db.open():
            QtWidgets.QMessageBox.critical(
                None,
                "Can't open db",
                'Click Cancel to exit',
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

    def execute_query_with_params(self, sql_query, query_values=None):
        query = QtSql.QSqlQuery()
        query.prepare(sql_query)

        if query_values:
            for query_value in query_values:
                query.addBindValue(query_value)

        query.exec()
        return query

    def add_new_operation_query(
        self, date, category, description, balance, status
    ):
        sql_query = ('''
            INSERT INTO finances (
                Date, Category, Description, Balance, Status
            ) VALUES (?, ?, ?, ?, ?)
        ''')
        self.execute_query_with_params(
            sql_query, [date, category, description, balance, status]
        )

    def update_operation_query(
        self, date, category, description, balance, status, id
    ):
        sql_query = (
            'UPDATE finances SET Date=?, Category=?, Description=?, '
            'Balance=?, Status=? WHERE ID=?'
        )
        self.execute_query_with_params(
            sql_query, [date, category, description, balance, status, id]
        )

    def delete_operation_query(self, id):
        sql_query = 'DELETE FROM finances WHERE ID=?'
        self.execute_query_with_params(sql_query, [id])

    def get_total(self, column, filter=None, value=None):
        sql_query = f'SELECT SUM ({column}) FROM finances'
        if filter and value:
            sql_query += f' WHERE {filter} = ?'

        query_values = []
        if value:
            query_values.append(value)

        query = self.execute_query_with_params(sql_query, query_values)

        if query.next():
            return str(query.value(0))
        return '0'

    def total_balance(self):
        return self.get_total(column='Balance')

    def total_income(self):
        return self.get_total(
            column='Balance', filter='Status', value='Доход'
        )

    def total_outcome(self):
        return self.get_total(
            column='Balance', filter='Status', value='Затраты'
        )

    def total_groceries(self):
        return self.get_total(
            column='Balance', filter='Category', value='Продукты'
        )

    def total_marketplace(self):
        return self.get_total(
            column='Balance', filter='Category', value='Маркетплейсы'
        )

    def total_transport(self):
        return self.get_total(
            column='Balance', filter='Category', value='Транспорт'
        )

    def total_entertainment(self):
        return self.get_total(
            column='Balance', filter='Category', value='Развлечения'
        )

    def total_other(self):
        return self.get_total(
            column='Balance', filter='Category', value='Другое'
        )
