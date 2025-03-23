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

    def category_exists(self, name: str) -> bool:
        """Проверяет, существует ли категория с таким именем."""
        query = QtSql.QSqlQuery(self.db)
        query.prepare('SELECT COUNT(*) FROM categories WHERE Name = ?')
        query.addBindValue(name)

        if query.exec() and query.next():
            return query.value(0) > 0
        return False

    def get_category_count(self) -> int:
        """Возвращает количество категорий в базе данных."""
        query = QtSql.QSqlQuery('SELECT COUNT(*) FROM categories', self.db)
        if query.exec() and query.next():
            return query.value(0)
        return 0

    def update_category(self, old_name: str, new_name: str) -> bool:
        """Обновляет название категории в базе данных."""
        query = QtSql.QSqlQuery(self.db)
        query.prepare('UPDATE categories SET Name = ? WHERE Name = ?')
        query.addBindValue(new_name)
        query.addBindValue(old_name)

        if not query.exec():
            print("Ошибка при обновлении категории:", query.lastError().text())
            return False
        return True
