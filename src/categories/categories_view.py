from PySide6.QtWidgets import QDialog

from src.categories.ui.categories_ui import Ui_Dialog


class CategoriesView(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
