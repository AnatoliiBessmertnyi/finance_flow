from PySide6.QtWidgets import QDialog

from src.categories.categories_handler import CategoriesHandler
from src.categories.categories_view import CategoriesView


class CategoriesController(QDialog):
    def __init__(self, view: 'CategoriesView', handler: 'CategoriesHandler',):
        super().__init__()
        self.view = view
        self.view.setupUi(self)

        self.handler = handler
