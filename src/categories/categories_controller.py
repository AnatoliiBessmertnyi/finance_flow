from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal

if TYPE_CHECKING:
    from src.categories.categories_handler import CategoriesHandler
    from src.categories.categories_view import CategoriesView


class CategoriesController(QObject):
    PROTECTED_CATEGORIES = [
        'Продукты',
        'Транспорт',
        'Жилье',
        'Развлечения',
        'Другое'
    ]
    category_deleted = Signal(str)
    category_updated = Signal(str, str)

    def __init__(
        self,
        view: 'CategoriesView',
        handler: 'CategoriesHandler',
    ):
        super().__init__()
        self.view = view
        self.handler = handler
        self.view.controller = self

        self.old_name = ''

        self.load_categories()
        self.connect_signals()

    def connect_signals(self) -> None:
        """Подключение сигналов к слотам."""
        self.view.new_btn.clicked.connect(self.on_add_category)
        self.view.delete_btn.clicked.connect(self.on_delete_category)
        self.view.table_container.cellChanged.connect(self.on_cell_changed)
        self.view.table_container.cellDoubleClicked.connect(
            self.on_cell_double_clicked
        )
        self.view.table_container.itemSelectionChanged.connect(
            self.protect_default_categoires
        )

    def load_categories(self):
        """Загружает категории из базы данных и отображает их в таблице."""
        categories = self.handler.fetch_all_categories()
        self.view.load_categories(categories)

    def protect_default_categoires(self):
        selected_items = self.view.table_container.selectedItems()
        if not selected_items:
            self.view.delete_btn.setEnabled(False)
            return

        selected_row = self.view.table_container.currentRow()
        category_name = self.view.table_container.item(selected_row, 0).text()
        self.view.delete_btn.setEnabled(
            category_name not in self.PROTECTED_CATEGORIES
        )

    def on_add_category(self):
        """Обрабатывает нажатие кнопки добавления категории."""
        category_name = self.view.get_category_name()
        if category_name:
            if self.handler.category_exists(category_name):
                self.view.show_error(
                    'Категория с таким именем уже существует.'
                )
                return

            if self.handler.get_category_count() >= 12:
                self.view.show_error('Достигнут лимит категорий (12 штук).')
                return

            self.view.table_container.cellChanged.disconnect(
                self.on_cell_changed
            )

            if self.handler.add_category(category_name):
                self.view.add_category_to_table(category_name)
                self.view.clear_input()

            self.view.table_container.cellChanged.connect(self.on_cell_changed)

    def on_delete_category(self):
        """Обрабатывает нажатие кнопки удаления категории."""
        selected_items = self.view.table_container.selectedItems()
        if selected_items:
            selected_row = self.view.table_container.currentRow()
            category_name = (
                self.view.table_container.item(selected_row, 0).text()
            )
            if self.handler.delete_category(category_name):
                self.view.table_container.removeRow(selected_row)
                self.category_deleted.emit(category_name)
                self.view.show_info(
                    f'Категория "{category_name}" успешно удалена.'
                )
        else:
            self.view.show_error('Не выбрана категория для удаления.')

    def on_cell_double_clicked(self, row: int, _):
        """Сохраняет старое значение перед редактированием."""
        self.old_name = self.view.table_container.item(row, 0).text()

    def on_cell_changed(self, row: int, column: int):
        """Обрабатывает изменение ячейки."""
        new_name = self.view.table_container.item(row, column).text().strip()

        if new_name and new_name != self.old_name:
            self.on_category_updated(self.old_name, new_name)

    def on_category_updated(self, old_name: str, new_name: str):
        """Обновляет название категории в базе данных."""
        if self.handler.category_exists(new_name):
            self.view.show_error('Категория с таким именем уже существует.')
            self.restore_old_name()
            return
        elif old_name in self.PROTECTED_CATEGORIES:
            self.view.show_error('Нельзя изменять системную категорию.')
            self.restore_old_name()
            return

        if self.handler.update_category(old_name, new_name):
            self.category_updated.emit(old_name, new_name)
            self.view.show_info(
                f'Категория "{old_name}" успешно обновлена на "{new_name}".'
            )
        else:
            self.view.show_error('Ошибка при обновлении категории.')
            self.load_categories()

    def restore_old_name(self):
        """Восстанавливает старое значение в таблице."""
        selected_row = self.view.table_container.currentRow()
        if selected_row >= 0:
            item = self.view.table_container.item(selected_row, 0)
            if item:
                item.setText(self.old_name)
