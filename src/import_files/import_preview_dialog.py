from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QCheckBox, QComboBox, QDialog, QHeaderView,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout)


class ImportPreviewDialog(QDialog):
    operations_imported = Signal(list)

    def __init__(self, operations, categories, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Проверка операций перед импортом')
        self.layout = QVBoxLayout(self)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ['Выбрать', 'Дата', 'Описание', 'Сумма', 'Категория']
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.categories = categories

        for op in operations:
            row = self.table.rowCount()
            self.table.insertRow(row)

            checkbox = QCheckBox()
            checkbox.setChecked(True)
            self.table.setCellWidget(row, 0, checkbox)

            self.table.setItem(
                row, 1, QTableWidgetItem(op['date'].strftime('%d.%m.%Y %H:%M'))
            )

            self.table.setItem(row, 2, QTableWidgetItem(op['description']))

            amount_item = QTableWidgetItem(str(op['balance']))
            amount_item.setTextAlignment(Qt.AlignRight)
            self.table.setItem(row, 3, amount_item)

            category_combo = QComboBox()
            category_combo.addItems(self.categories)
            self.table.setCellWidget(row, 4, category_combo)

        self.import_btn = QPushButton('Загрузить выбранные операции')
        self.import_btn.clicked.connect(self.prepare_import)

        self.layout.addWidget(self.table)
        self.layout.addWidget(self.import_btn)

    def prepare_import(self):
        operations_to_import = []
        for row in range(self.table.rowCount()):
            if self.table.cellWidget(row, 0).isChecked():
                operations_to_import.append({
                    'date': self.table.item(row, 1).text(),
                    'description': self.table.item(row, 2).text(),
                    'balance': float(self.table.item(row, 3).text()),
                    'category': self.table.cellWidget(row, 4).currentText()
                })
        self.operations_imported.emit(operations_to_import)
        self.accept()
