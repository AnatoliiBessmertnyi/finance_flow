from PySide6 import QtWidgets
from src.operations.ui.new_operation_ui import Ui_Dialog


class OperationsView(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
