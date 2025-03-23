# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_operation.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QComboBox,
    QDateTimeEdit, QDialog, QFrame, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 300)
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

        self.category_cb = QComboBox(self.operation_frame)
        self.category_cb.setObjectName(u"category_cb")
        self.category_cb.setStyleSheet(u"QComboBox {\n"
"font-size: 14px;\n"
"color: #c8fafa;\n"
"padding-left: 8px;\n"
"}\n"
"\n"
"QComboBox:item {\n"
"color: #c8fafa;;\n"
"padding-left: 8px;\n"
"}")

        self.verticalLayout.addWidget(self.category_cb)

        self.date = QDateTimeEdit(self.operation_frame)
        self.date.setObjectName(u"date")
        self.date.setStyleSheet(u"font-size: 14px;\n"
"color: #c8fafa;\n"
"padding-left: 8px;;\n"
"\n"
"\n"
"")
        self.date.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.date.setDate(QDate(2025, 1, 1))

        self.verticalLayout.addWidget(self.date)

        self.description_le = QLineEdit(self.operation_frame)
        self.description_le.setObjectName(u"description_le")
        self.description_le.setStyleSheet(u"font-size: 14px;\n"
"color: #c8fafa;\n"
"padding-left: 8px;")

        self.verticalLayout.addWidget(self.description_le)

        self.amount_le = QLineEdit(self.operation_frame)
        self.amount_le.setObjectName(u"amount_le")
        self.amount_le.setStyleSheet(u"font-size: 14px;\n"
"color: #c8fafa;\n"
"padding-left: 8px;")

        self.verticalLayout.addWidget(self.amount_le)

        self.operation_type_cb = QComboBox(self.operation_frame)
        self.operation_type_cb.addItem("")
        self.operation_type_cb.addItem("")
        self.operation_type_cb.setObjectName(u"operation_type_cb")
        self.operation_type_cb.setStyleSheet(u"QComboBox {\n"
"font-size: 14px;\n"
"color: #c8fafa;\n"
"padding-left: 8px;\n"
"}\n"
"\n"
"QComboBox:item {\n"
"color: white;\n"
"padding-left: 8px;\n"
"}")

        self.verticalLayout.addWidget(self.operation_type_cb)

        self.reload_cb = QCheckBox(self.operation_frame)
        self.reload_cb.setObjectName(u"reload_cb")
        self.reload_cb.setStyleSheet(u"font-size: 14px;\n"
"color: #c8fafa;\n"
"padding-left: 10px;")

        self.verticalLayout.addWidget(self.reload_cb)

        self.pushButton = QPushButton(self.operation_frame)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.pushButton)


        self.verticalLayout_2.addWidget(self.operation_frame)


        self.retranslateUi(Dialog)

        self.category_cb.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"new_operation", None))
        self.title_lbl.setText(QCoreApplication.translate("Dialog", u"\u041d\u043e\u0432\u0430\u044f \u043e\u043f\u0435\u0440\u0430\u0446\u0438\u044f", None))
        self.category_cb.setPlaceholderText(QCoreApplication.translate("Dialog", u"\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044e", None))
        self.description_le.setPlaceholderText(QCoreApplication.translate("Dialog", u"\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435", None))
        self.amount_le.setPlaceholderText(QCoreApplication.translate("Dialog", u"\u0421\u0443\u043c\u043c\u0430", None))
        self.operation_type_cb.setItemText(0, QCoreApplication.translate("Dialog", u"\u0414\u043e\u0445\u043e\u0434", None))
        self.operation_type_cb.setItemText(1, QCoreApplication.translate("Dialog", u"\u0417\u0430\u0442\u0440\u0430\u0442\u044b", None))

        self.reload_cb.setText(QCoreApplication.translate("Dialog", u"\u0415\u0436\u0435\u043c\u0435\u0441\u044f\u0447\u043d\u0430\u044f \u043e\u043f\u0435\u0440\u0430\u0446\u0438\u044f", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043e\u043f\u0435\u0440\u0430\u0446\u0438\u044e", None))
    # retranslateUi

