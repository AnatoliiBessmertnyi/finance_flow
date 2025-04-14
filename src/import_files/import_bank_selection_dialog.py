from PySide6.QtWidgets import (QComboBox, QDialog, QLabel, QPushButton,
                               QVBoxLayout)


class BankSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Выбор банка')
        self.layout = QVBoxLayout(self)

        self.label = QLabel('Выберите банк, из которого загружаете выписку:')
        self.bank_combo = QComboBox()
        self.bank_combo.addItems(['Тинькофф', 'Сбербанк', 'Альфа-Банк'])
        self.ok_btn = QPushButton('Продолжить')

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.bank_combo)
        self.layout.addWidget(self.ok_btn)

        self.ok_btn.clicked.connect(self.accept)
