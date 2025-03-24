from PySide6 import QtSql


class OperationsHandler:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def add_operation(self, date, category, description, balance):
        """Добавляет новую операцию."""
        query = '''
            INSERT INTO finances (Date, Category, Description, Balance)
            VALUES (?, ?, ?, ?)
        '''
        self.db_handler.execute_query(
            query, [date, category, description, balance]
        )

    def edit_operation(
        self, operation_id, date, category, description, balance
    ):
        """Редактирует существующую операцию."""
        query = '''
            UPDATE finances
            SET Date=?, Category=?, Description=?, Balance=?
            WHERE ID=?
        '''
        self.db_handler.execute_query(
            query, [date, category, description, balance, operation_id]
        )

    def delete_operation(self, operation_id):
        """Удаляет операцию по ID."""
        query = 'DELETE FROM finances WHERE ID=?'
        self.db_handler.execute_query(query, [operation_id])

    def get_operation_by_id(self, operation_id):
        """Возвращает данные операции по ID."""
        query = self.db_handler.execute_query(
            'SELECT * FROM finances WHERE ID = ?', [operation_id]
        )
        if query.next():
            return {
                'id': query.value('ID'),
                'date': query.value('Date'),
                'category': query.value('Category'),
                'description': query.value('Description'),
                'balance': query.value('Balance')
            }
        return None

    def get_all_categories(self) -> list:
        """Возвращает список всех категорий из базы данных."""
        query = QtSql.QSqlQuery(
            'SELECT Name FROM categories', self.db_handler.db
        )
        categories = []
        while query.next():
            categories.append(query.value(0))
        return categories
