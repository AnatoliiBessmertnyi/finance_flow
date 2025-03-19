class OperationsHandler:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def add_operation(self, date, category, description, balance, status):
        """Добавляет новую операцию."""
        query = '''
            INSERT INTO finances (Date, Category, Description, Balance, Status)
            VALUES (?, ?, ?, ?, ?)
        '''
        self.db_handler.execute_query(
            query, [date, category, description, balance, status]
        )

    def edit_operation(
        self, operation_id, date, category, description, balance, status
    ):
        """Редактирует существующую операцию."""
        query = '''
            UPDATE finances
            SET Date=?, Category=?, Description=?, Balance=?, Status=?
            WHERE ID=?
        '''
        self.db_handler.execute_query(
            query, [date, category, description, balance, status, operation_id]
        )

    def delete_operation(self, operation_id):
        """Удаляет операцию по ID."""
        query = 'DELETE FROM finances WHERE ID=?'
        self.db_handler.execute_query(query, [operation_id])
