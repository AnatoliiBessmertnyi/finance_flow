from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QDialog, QFileDialog, QLabel, QMessageBox,
                               QPushButton, QVBoxLayout)


class FileSelectionDialog(QDialog):
    def __init__(self, bank_name, parent=None):
        super().__init__(parent)
        self.bank_name = bank_name
        self.file_path = None
        self.setWindowTitle(f'Загрузка выписки ({bank_name})')
        self.setAcceptDrops(True)

        self.layout = QVBoxLayout(self)

        self.label = QLabel(
            'Перетащите PDF-файл сюда или нажмите "Выбрать файл"'
        )
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet('border: 2px dashed #aaa; padding: 20px;')

        self.select_btn = QPushButton('Выбрать файл')
        self.select_btn.clicked.connect(self.open_file_dialog)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.select_btn)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls and urls[0].toLocalFile().endswith('.pdf'):
            self.file_path = urls[0].toLocalFile()
            self.accept()
        else:
            QMessageBox.warning(
                self, 'Ошибка', 'Файл должен быть в формате PDF!'
            )

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Выберите выписку', '', 'PDF Files (*.pdf)'
        )
        if file_path:
            self.file_path = file_path
            self.accept()
