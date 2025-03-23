from PySide6.QtWidgets import QDialog

from src.operations.ui.new_operation_ui import Ui_Dialog


class OperationsView(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
