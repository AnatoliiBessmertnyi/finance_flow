from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QHeaderView, QTableWidgetItem

from src.categories.ui.categories_ui import Ui_Dialog


class CategoriesView(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.table_container.setColumnCount(1)
        self.table_container.setHorizontalHeaderLabels(["Категория"])
        self.table_container.verticalHeader().setVisible(False)
        self.table_container.horizontalHeader().setVisible(False)
        self.table_container.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.new_btn.clicked.connect(self.on_add_category)
        self.delete_btn.clicked.connect(self.on_delete_category)

    def on_add_category(self):
        """Обрабатывает нажатие кнопки добавления категории."""
        category_name = self.category_name_te.toPlainText().strip()
        if category_name:
            if self.controller.add_category(category_name):
                self.add_category_to_table(category_name)
                self.category_name_te.clear()

    def add_category_to_table(self, name: str):
        """Добавляет категорию в таблицу."""
        row_position = self.table_container.rowCount()
        self.table_container.insertRow(row_position)

        item = QTableWidgetItem(name)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table_container.setItem(row_position, 0, item)

    def load_categories(self, categories: list):
        """Загружает список категорий в таблицу."""
        self.table_container.setRowCount(0)
        for category in categories:
            self.add_category_to_table(category)

    def on_delete_category(self):
        """Обрабатывает нажатие кнопки удаления категории."""
        selected_row = self.table_container.currentRow()
        if selected_row >= 0:
            category_item = self.table_container.item(selected_row, 0)
            category_name = category_item.text()

            if self.controller.delete_category(category_name):
                self.table_container.removeRow(selected_row)
        else:
            print("Ошибка: Не выбрана категория для удаления.")
