from PySide6 import QtSql
from datetime import datetime


class OperationsHandler:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def add_operation(self, date, category, description, balance):
        """Добавляет новую операцию."""
        if isinstance(date, str):
            date_obj = datetime.strptime(date, "%d.%m.%Y %H:%M")
            date = date_obj.strftime("%Y-%m-%d %H:%M")
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
        if isinstance(date, str):
            date_obj = datetime.strptime(date, "%d.%m.%Y %H:%M")
            date = date_obj.strftime("%Y-%m-%d %H:%M")
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
        other_category = None

        while query.next():
            category = query.value(0)
            if category == 'Другое':
                other_category = category
            else:
                categories.append(category)

        categories.sort()
        if other_category:
            categories.append(other_category)

        return categories

    def update_operations_category(
        self, old_category: str, new_category: str
    ) -> bool:
        """Обновляет категорию во всех операциях, где она использовалась."""
        query = '''
            UPDATE finances
            SET Category=?
            WHERE Category=?
        '''
        return self.db_handler.execute_query(
            query, [new_category, old_category]
        )

    def get_operations_count_by_category(self, category: str) -> int:
        """Возвращает количество операций с указанной категорией."""
        query = QtSql.QSqlQuery(self.db_handler.db)
        query.prepare('SELECT COUNT(*) FROM finances WHERE Category=?')
        query.addBindValue(category)
        if query.exec() and query.next():
            return query.value(0)
        return 0
