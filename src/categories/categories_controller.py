from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.categories.categories_handler import CategoriesHandler
    from src.categories.categories_view import CategoriesView


class CategoriesController:
    def __init__(self, view: 'CategoriesView', handler: 'CategoriesHandler'):
        self.view = view
        self.handler = handler
        self.view.controller = self

        self.load_categories()
        self.connect_signals()

    def connect_signals(self) -> None:
        """Подключение сигналов к слотам."""
        self.view.new_btn.clicked.connect(self.on_add_category)
        self.view.delete_btn.clicked.connect(self.on_delete_category)
        self.view.category_updated.connect(self.on_category_updated)

    def load_categories(self):
        """Загружает категории из базы данных и отображает их в таблице."""
        categories = self.handler.fetch_all_categories()
        self.view.load_categories(categories)

    def on_add_category(self):
        """Обрабатывает нажатие кнопки добавления категории."""
        category_name = self.view.get_category_name()
        if category_name:
            if self.handler.category_exists(category_name):
                self.view.show_error("Категория с таким именем уже существует.")
                return

            if self.handler.get_category_count() >= 10:
                self.view.show_error("Достигнут лимит категорий (10 штук).")
                return

            if self.handler.add_category(category_name):
                self.view.add_category_to_table(category_name)
                self.view.clear_input()

    def on_delete_category(self):
        """Обрабатывает нажатие кнопки удаления категории."""
        category_name = self.view.get_selected_category()
        if category_name:
            if self.handler.delete_category(category_name):
                self.load_categories()
        else:
            self.view.show_error("Не выбрана категория для удаления.")

    def on_category_updated(self, old_name: str, new_name: str):
        """Обновляет название категории в базе данных."""
        print('on_category_updated')
        if self.handler.category_exists(new_name):
            self.view.show_error("Категория с таким именем уже существует.")
            self.load_categories()
            return

        if self.handler.update_category(old_name, new_name):
            print(f"Категория '{old_name}' успешно обновлена на '{new_name}'.")
        else:
            self.view.show_error("Ошибка при обновлении категории.")
            self.load_categories()
