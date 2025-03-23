from PySide6 import QtSql


class CategoriesHandler:
    def __init__(self, parent_handler):
        self.db = parent_handler.db

    def add_category(self, name: str) -> bool:
        """Добавляет новую категорию в базу данных."""
        query = QtSql.QSqlQuery(self.db)
        query.prepare('INSERT INTO categories (Name) VALUES (?)')
        query.addBindValue(name)

        if not query.exec():
            print("Ошибка при добавлении категории:", query.lastError().text())
            return False
        return True

    def fetch_all_categories(self) -> list:
        """Возвращает список всех категорий из базы данных."""
        query = QtSql.QSqlQuery('SELECT Name FROM categories', self.db)
        categories = []
        while query.next():
            categories.append(query.value(0))
        return categories

    def delete_category(self, name: str) -> bool:
        """Удаляет категорию из базы данных."""
        query = QtSql.QSqlQuery(self.db)
        query.prepare('DELETE FROM categories WHERE Name = ?')
        query.addBindValue(name)

        if not query.exec():
            print("Ошибка при удалении категории:", query.lastError().text())
            return False
        return True
