from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QCheckBox, QComboBox, QDialog, QHBoxLayout,
                               QHeaderView, QPushButton, QTableWidget,
                               QTableWidgetItem, QVBoxLayout)


class ImportPreviewDialog(QDialog):
    operations_imported = Signal(list)

    CATEGORY_RULES = {
        'Еда': {
            'кфс', 'макдоналдс', 'бургер кинг', 'кофе', 'kofe', 'coffee', 'doner',
            'makovka'
        },
        'Транспорт': {
            'такси', 'убер', 'метро', 'автобус', 'тройка', 'strelkacard'
        },
        'Продукты': {'pyaterochka'},
        'Здоровье': {'apteka', 'gorzdrav', 'aptechnoe'},
    }

    def __init__(self, operations, categories, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Проверка операций перед импортом')
        self.setMinimumWidth(600)
        self.layout = QVBoxLayout(self)

        self.header_container = QHBoxLayout()
        self.header_container.addStretch(1)
        self.select_all_checkbox = QCheckBox('Выбрать все')
        self.select_all_checkbox.setChecked(True)
        self.select_all_checkbox.stateChanged.connect(self.toggle_select_all)
        self.header_container.addWidget(self.select_all_checkbox)
        self.layout.addLayout(self.header_container)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ['Дата', 'Описание', 'Сумма', 'Категория', 'Выбрать']
        )
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 200)
        self.table.setColumnWidth(4, 60)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Fixed)

        self.categories = categories

        for op in operations:
            row = self.table.rowCount()
            self.table.insertRow(row)

            self.table.setItem(
                row, 0, QTableWidgetItem(op['date'].strftime('%d.%m.%Y %H:%M'))
            )

            self.table.setItem(row, 1, QTableWidgetItem(op['description']))

            amount_item = QTableWidgetItem(str(op['balance']))
            amount_item.setTextAlignment(Qt.AlignRight)
            self.table.setItem(row, 2, amount_item)

            category_combo = QComboBox()
            category_combo.addItems(self.categories)
            auto_category = self.detect_category(op['description'], op['balance'])
            if auto_category:
                index = category_combo.findText(auto_category)
            else:
                index = category_combo.findText('Другое')

            if index >= 0:
                category_combo.setCurrentIndex(index)
            self.table.setCellWidget(row, 3, category_combo)

            checkbox = QCheckBox()
            checkbox.setChecked(True)
            self.table.setCellWidget(row, 4, checkbox)

        self.import_btn = QPushButton('Загрузить выбранные операции')
        self.import_btn.clicked.connect(self.prepare_import)

        self.layout.addWidget(self.table)
        self.layout.addWidget(self.import_btn)

    def toggle_select_all(self, state: int):
        """Обработчик для чекбокса Выбрать все."""
        for row in range(self.table.rowCount()):
            checkbox = self.table.cellWidget(row, 4)
            checkbox.setChecked(bool(state))

    def detect_category(self, description: str, amount: float) -> str | None:
        """Автоматически определяет категорию по описанию и сумме операции"""
        description_lower = description.lower()

        if ('внутренний перевод' in description_lower
                and amount == -250):
            return 'Транспорт'

        for category, keywords in self.CATEGORY_RULES.items():
            if any(keyword in description_lower for keyword in keywords):
                return category

    def prepare_import(self) -> None:
        operations_to_import = []
        for row in range(self.table.rowCount()):
            if self.table.cellWidget(row, 4).isChecked():
                operations_to_import.append({
                    'date': self.table.item(row, 0).text(),
                    'description': self.table.item(row, 1).text(),
                    'balance': float(self.table.item(row, 2).text()),
                    'category': self.table.cellWidget(row, 3).currentText()
                })
        self.operations_imported.emit(operations_to_import)
        self.accept()
