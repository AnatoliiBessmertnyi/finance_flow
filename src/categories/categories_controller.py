from typing import TYPE_CHECKING

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QDialog

if TYPE_CHECKING:
    from src.categories.categories_handler import CategoriesHandler
    from src.categories.categories_view import CategoriesView


class CategoriesController:
    def __init__(self, view: 'CategoriesView', handler: 'CategoriesHandler'):
        super().__init__()
        self.view = view
        self.handler = handler

        self.view.controller = self

        self.load_categories()

    def load_categories(self):
        """Загружает категории из базы данных и отображает их в таблице."""
        categories = self.handler.fetch_all_categories()
        self.view.load_categories(categories)

    def add_category(self, name: str) -> bool:
        """Добавляет новую категорию в базу данных."""
        if self.handler.add_category(name):
            return True
        return False

    def delete_category(self, name: str) -> bool:
        """Удаляет категорию из базы данных."""
        return self.handler.delete_category(name)
