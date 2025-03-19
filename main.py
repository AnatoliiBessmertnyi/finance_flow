import sys

from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtSql import QSqlTableModel

from connection import Data
from src.main_window.ui.main_window_ui import Ui_MainWindow
from src.widgets.new_operation_ui import Ui_Dialog


class OperationTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.conn = Data()
        self.view_data()
        self.reload_data()

        self.ui.new_btn.clicked.connect(self.open_new_operation_window)
        self.ui.edit_btn.clicked.connect(self.open_new_operation_window)
        self.ui.delete_btn.clicked.connect(self.delete_current_operation)

    def view_data(self):
        self.model = QSqlTableModel(self)
        self.model.setTable('finances')
        self.model.select()
        self.ui.table_container.setModel(self.model)

    def reload_data(self):
        self.ui.balance_lbl.setText(self.conn.total_balance())
        self.ui.income_balance_lbl.setText(self.conn.total_income())
        self.ui.outcome_balance_lbl.setText(self.conn.total_outcome())
        self.ui.groceries_balance.setText(self.conn.total_groceries())
        self.ui.marketplace_balance.setText(self.conn.total_marketplace())
        self.ui.transport_balance.setText(self.conn.total_transport())
        self.ui.entertainment_balance.setText(self.conn.total_entertainment())
        self.ui.other_balance.setText(self.conn.total_other())

    def open_new_operation_window(self):
        self.new_window = QtWidgets.QDialog()
        self.ui_window = Ui_Dialog()
        self.ui_window.setupUi(self.new_window)
        self.new_window.show()
        sender = self.sender()
        if sender.text() == 'Новая операция':
            self.ui_window.pushButton.clicked.connect(self.add_new_operation)
        else:
            self.ui_window.pushButton.clicked.connect(
                self.edit_current_operation
            )

    def add_new_operation(self):
        date = self.ui_window.date.text()
        category = self.ui_window.category_cb.currentText()
        description = self.ui_window.description_le.text()
        balance = self.ui_window.amount_le.text()
        status = self.ui_window.operation_type_cb.currentText()

        self.conn.add_new_operation_query(
            date, category, description, balance, status
        )
        self.reload_data()
        self.view_data()
        self.new_window.close()

    def edit_current_operation(self):
        index = self.ui.table_container.selectedIndexes()[0]
        id = str(self.ui.table_container.model().data(index))
        date = self.ui_window.date.text()
        category = self.ui_window.category_cb.currentText()
        description = self.ui_window.description_le.text()
        balance = self.ui_window.amount_le.text()
        status = self.ui_window.operation_type_cb.currentText()

        self.conn.update_operation_query(
            date, category, description, balance, status, id
        )
        self.reload_data()
        self.view_data()
        self.new_window.close()

    def delete_current_operation(self):
        index = self.ui.table_container.selectedIndexes()[0]
        id = str(self.ui.table_container.model().data(index))

        self.conn.delete_operation_query(id)
        self.reload_data()
        self.view_data()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OperationTracker()
    window.show()
    sys.exit(app.exec())
