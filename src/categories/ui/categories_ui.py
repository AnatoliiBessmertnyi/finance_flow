# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'categories.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QPushButton, QSizePolicy,
    QTableWidget, QTableWidgetItem, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(244, 300)
        Dialog.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0 rgba(0, 102, 102, 255), stop:1 rgba(0, 191, 255, 255));\n"
"font-family: Roboto;")
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.operation_frame = QFrame(Dialog)
        self.operation_frame.setObjectName(u"operation_frame")
        self.operation_frame.setStyleSheet(u"background-color: rgba(255, 255, 255, 30);\n"
"border: 1px solid rgba(255, 255, 255, 40);\n"
"border-radius: 6px;")
        self.operation_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.operation_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.operation_frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.title_lbl = QLabel(self.operation_frame)
        self.title_lbl.setObjectName(u"title_lbl")
        self.title_lbl.setStyleSheet(u"color: #c8fafa;\n"
"font-weight: bold;\n"
"font-size: 18px;\n"
"background-color: none;\n"
"border: none;\n"
"")
        self.title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.title_lbl)

        self.category_name_te = QTextEdit(self.operation_frame)
        self.category_name_te.setObjectName(u"category_name_te")
        self.category_name_te.setMinimumSize(QSize(0, 28))
        self.category_name_te.setMaximumSize(QSize(16777215, 28))
        self.category_name_te.setStyleSheet(u"color: #c8fafa;\n"
"font-size: 14px;")

        self.verticalLayout.addWidget(self.category_name_te)

        self.table_container = QTableWidget(self.operation_frame)
        self.table_container.setObjectName(u"table_container")
        self.table_container.setStyleSheet(u"QTableView {\n"
"background-color: rgba(255, 255, 255, 30);\n"
"border: 1px solid  rgba(255, 255, 255, 40);\n"
"border-bottom-left-radius: 6px;\n"
"border-bottom-right-radius: 6px;\n"
"}\n"
"QTableView::section {\n"
"background-color: rgb(53, 53, 53);\n"
"color: #c8fafa;\n"
"border: none;\n"
"height: 50px;\n"
"font-size: 14px;\n"
"}\n"
"\n"
"QTableView::item {\n"
"border-style: none;\n"
"border-bottom:  rgba(255, 255, 255, 50);\n"
"}\n"
"\n"
"QTableView::item:selected {\n"
"border: none;\n"
"color: #E0F7FA;\n"
"background-color: rgba(255, 255, 255, 50);\n"
"}")
        self.table_container.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.table_container.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table_container.setShowGrid(False)
        self.table_container.setSortingEnabled(True)

        self.verticalLayout.addWidget(self.table_container)

        self.buttons_container = QHBoxLayout()
        self.buttons_container.setSpacing(4)
        self.buttons_container.setObjectName(u"buttons_container")
        self.new_btn = QPushButton(self.operation_frame)
        self.new_btn.setObjectName(u"new_btn")
        self.new_btn.setMinimumSize(QSize(100, 52))
        self.new_btn.setMaximumSize(QSize(16777215, 52))
        self.new_btn.setStyleSheet(u"QPushButton {\n"
"color: #c8fafa;\n"
"background-color: rgba(255, 255, 255, 30);\n"
"border: 1px solid rgba(255, 255, 255, 40);\n"
"border-radius: 6px;\n"
"width: 230px;\n"
"height: 50px;\n"
"}\n"
"QPushButton:hover {\n"
"background-color: rgba(255, 255, 255, 40);\n"
"}\n"
"QPushButton:pressed {\n"
"background-color: rgba(255, 255, 255, 70);\n"
"}\n"
"\n"
"")
        self.new_btn.setIconSize(QSize(24, 24))

        self.buttons_container.addWidget(self.new_btn)

        self.delete_btn = QPushButton(self.operation_frame)
        self.delete_btn.setObjectName(u"delete_btn")
        self.delete_btn.setMinimumSize(QSize(100, 52))
        self.delete_btn.setMaximumSize(QSize(16777215, 52))
        self.delete_btn.setStyleSheet(u"QPushButton {\n"
"color: #c8fafa;\n"
"background-color: rgba(255, 255, 255, 30);\n"
"border: 1px solid rgba(255, 255, 255, 40);\n"
"border-radius: 6px;\n"
"width: 230px;\n"
"height: 50px;\n"
"}\n"
"QPushButton:hover {\n"
"background-color: rgba(255, 255, 255, 40);\n"
"}\n"
"QPushButton:pressed {\n"
"background-color: rgba(255, 255, 255, 70);\n"
"}\n"
"\n"
"")
        self.delete_btn.setIconSize(QSize(24, 24))

        self.buttons_container.addWidget(self.delete_btn)


        self.verticalLayout.addLayout(self.buttons_container)


        self.verticalLayout_2.addWidget(self.operation_frame)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"new_operation", None))
        self.title_lbl.setText(QCoreApplication.translate("Dialog", u"\u041d\u043e\u0432\u0430\u044f \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f", None))
        self.category_name_te.setPlaceholderText(QCoreApplication.translate("Dialog", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u0438\u043c\u044f \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438", None))
        self.new_btn.setText(QCoreApplication.translate("Dialog", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None))
        self.delete_btn.setText(QCoreApplication.translate("Dialog", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c", None))
    # retranslateUi

