from PySide6.QtWidgets import (QDialog, QHeaderView, QMessageBox,
                               QTableWidgetItem)

from src.categories.ui.categories_ui import Ui_Dialog


class CategoriesView(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.table_container.setColumnCount(1)
        self.table_container.setHorizontalHeaderLabels(["Категория"])
        self.table_container.verticalHeader().setVisible(False)
        self.table_container.horizontalHeader().setVisible(False)
        self.table_container.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

    def add_category_to_table(self, name: str):
        """Добавляет категорию в таблицу."""
        row_position = self.table_container.rowCount()
        self.table_container.insertRow(row_position)

        item = QTableWidgetItem(name)
        self.table_container.setItem(row_position, 0, item)

    def load_categories(self, categories: list):
        """Загружает список категорий в таблицу."""
        self.table_container.setRowCount(0)
        for category in categories:
            self.add_category_to_table(category)

    def clear_input(self):
        """Очищает поле ввода."""
        self.category_name_te.clear()

    def show_error(self, message: str):
        """Показывает сообщение об ошибке."""
        QMessageBox.warning(self, "Ошибка", message)

    def get_category_name(self) -> str:
        """Возвращает текст из поля ввода."""
        return self.category_name_te.toPlainText().strip()

    def get_selected_category(self) -> str:
        """Возвращает выбранную категорию."""
        selected_row = self.table_container.currentRow()
        if selected_row >= 0:
            category_item = self.table_container.item(selected_row, 0)
            return category_item.text()
        return ""
