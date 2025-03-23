# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QTableView, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(728, 600)
        MainWindow.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0 rgba(0, 102, 102, 255), stop:1 rgba(0, 191, 255, 255));\n"
"font-family: Roboto;")
        self.main_widget = QWidget(MainWindow)
        self.main_widget.setObjectName(u"main_widget")
        self.verticalLayout_3 = QVBoxLayout(self.main_widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.header_container = QHBoxLayout()
        self.header_container.setObjectName(u"header_container")
        self.balance_frame = QFrame(self.main_widget)
        self.balance_frame.setObjectName(u"balance_frame")
        self.balance_frame.setStyleSheet(u"background-color: rgba(255, 255, 255, 30);\n"
"border: 1px solid rgba(255, 255, 255, 40);\n"
"border-radius: 6px;")
        self.verticalLayout = QVBoxLayout(self.balance_frame)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(8, 8, 8, 8)
        self.balance_title_lbl = QLabel(self.balance_frame)
        self.balance_title_lbl.setObjectName(u"balance_title_lbl")
        self.balance_title_lbl.setStyleSheet(u"color: #c8fafa;\n"
"font-weight: bold;\n"
"font-size: 18px;\n"
"background-color: none;\n"
"border: none;\n"
"")

        self.verticalLayout.addWidget(self.balance_title_lbl)

        self.balance_lbl = QLabel(self.balance_frame)
        self.balance_lbl.setObjectName(u"balance_lbl")
        self.balance_lbl.setStyleSheet(u"color: #c8fafa;\n"
"font-size: 28px;\n"
"background-color: none;\n"
"border: none;\n"
"")

        self.verticalLayout.addWidget(self.balance_lbl)

        self.income_container = QHBoxLayout()
        self.income_container.setSpacing(0)
        self.income_container.setObjectName(u"income_container")
        self.income_container.setContentsMargins(-1, 7, -1, -1)
        self.income_icon = QLabel(self.balance_frame)
        self.income_icon.setObjectName(u"income_icon")
        self.income_icon.setMaximumSize(QSize(24, 16777215))
        self.income_icon.setStyleSheet(u"background-color: none;\n"
"border: none;\n"
"padding-top: 10px;")
        self.income_icon.setPixmap(QPixmap(u":/icons/arrow_insert.svg"))

        self.income_container.addWidget(self.income_icon)

        self.income_lbl = QLabel(self.balance_frame)
        self.income_lbl.setObjectName(u"income_lbl")
        self.income_lbl.setStyleSheet(u"color: #c8fafa;\n"
"font-size: 16px;\n"
"background-color: none;\n"
"border: none;\n"
"font-weight: bold;\n"
"padding-top: 10px;")

        self.income_container.addWidget(self.income_lbl)


        self.verticalLayout.addLayout(self.income_container)

        self.income_balance_lbl = QLabel(self.balance_frame)
        self.income_balance_lbl.setObjectName(u"income_balance_lbl")
        self.income_balance_lbl.setStyleSheet(u"color: #c8fafa;\n"
"font-size: 22px;\n"
"background-color: none;\n"
"border: none;\n"
"")

        self.verticalLayout.addWidget(self.income_balance_lbl)

        self.outcome_container = QHBoxLayout()
        self.outcome_container.setSpacing(0)
        self.outcome_container.setObjectName(u"outcome_container")
        self.outcome_container.setContentsMargins(-1, 7, -1, -1)
        self.outcome_icon = QLabel(self.balance_frame)
        self.outcome_icon.setObjectName(u"outcome_icon")
        self.outcome_icon.setMaximumSize(QSize(24, 16777215))
        self.outcome_icon.setStyleSheet(u"background-color: none;\n"
"border: none;")
        self.outcome_icon.setPixmap(QPixmap(u":/icons/call_received.svg"))

        self.outcome_container.addWidget(self.outcome_icon)

        self.outcome_lbl = QLabel(self.balance_frame)
        self.outcome_lbl.setObjectName(u"outcome_lbl")
        self.outcome_lbl.setStyleSheet(u"color: #c8fafa;\n"
"font-size: 16px;\n"
"background-color: none;\n"
"border: none;\n"
"font-weight: bold;")

        self.outcome_container.addWidget(self.outcome_lbl)


        self.verticalLayout.addLayout(self.outcome_container)

        self.outcome_balance_lbl = QLabel(self.balance_frame)
        self.outcome_balance_lbl.setObjectName(u"outcome_balance_lbl")
        self.outcome_balance_lbl.setStyleSheet(u"color: #c8fafa;\n"
"font-size: 22px;\n"
"background-color: none;\n"
"border: none;\n"
"")

        self.verticalLayout.addWidget(self.outcome_balance_lbl)


        self.header_container.addWidget(self.balance_frame)

        self.category_frame = QFrame(self.main_widget)
        self.category_frame.setObjectName(u"category_frame")
        self.category_frame.setStyleSheet(u"background-color: rgba(255, 255, 255, 30);\n"
"border: 1px solid rgba(255, 255, 255, 40);\n"
"border-radius: 6px;")
        self.verticalLayout_2 = QVBoxLayout(self.category_frame)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(8, 8, 8, 8)
        self.title_container = QHBoxLayout()
        self.title_container.setObjectName(u"title_container")
        self.category_title_lbl = QLabel(self.category_frame)
        self.category_title_lbl.setObjectName(u"category_title_lbl")
        self.category_title_lbl.setStyleSheet(u"color: #c8fafa;\n"
"font-weight: bold;\n"
"font-size: 18px;\n"
"background-color: none;\n"
"border: none;\n"
"")

        self.title_container.addWidget(self.category_title_lbl)

        self.category_edit_btn = QPushButton(self.category_frame)
        self.category_edit_btn.setObjectName(u"category_edit_btn")
        self.category_edit_btn.setMinimumSize(QSize(24, 24))
        self.category_edit_btn.setMaximumSize(QSize(24, 24))
        self.category_edit_btn.setStyleSheet(u"color: #c8fafa;\n"
"width: 230px;\n"
"height: 50px;\n"
"background-color: none;\n"
"border: none;\n"
"")

        self.title_container.addWidget(self.category_edit_btn)


        self.verticalLayout_2.addLayout(self.title_container)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.header_container.addWidget(self.category_frame)


        self.verticalLayout_3.addLayout(self.header_container)

        self.buttons_container = QHBoxLayout()
        self.buttons_container.setObjectName(u"buttons_container")
        self.new_btn = QPushButton(self.main_widget)
        self.new_btn.setObjectName(u"new_btn")
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
        icon = QIcon()
        icon.addFile(u":/icons/add.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.new_btn.setIcon(icon)
        self.new_btn.setIconSize(QSize(24, 24))

        self.buttons_container.addWidget(self.new_btn)

        self.edit_btn = QPushButton(self.main_widget)
        self.edit_btn.setObjectName(u"edit_btn")
        self.edit_btn.setStyleSheet(u"QPushButton {\n"
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
        icon1 = QIcon()
        icon1.addFile(u":/icons/edit.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.edit_btn.setIcon(icon1)
        self.edit_btn.setIconSize(QSize(24, 24))

        self.buttons_container.addWidget(self.edit_btn)

        self.delete_btn = QPushButton(self.main_widget)
        self.delete_btn.setObjectName(u"delete_btn")
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
        icon2 = QIcon()
        icon2.addFile(u":/icons/delete.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.delete_btn.setIcon(icon2)
        self.delete_btn.setIconSize(QSize(24, 24))

        self.buttons_container.addWidget(self.delete_btn)


        self.verticalLayout_3.addLayout(self.buttons_container)

        self.table_container = QTableView(self.main_widget)
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
        self.table_container.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table_container.setShowGrid(False)
        self.table_container.setSortingEnabled(True)

        self.verticalLayout_3.addWidget(self.table_container)

        MainWindow.setCentralWidget(self.main_widget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Finance tracker", None))
        self.balance_title_lbl.setText(QCoreApplication.translate("MainWindow", u"\u0422\u0435\u043a\u0443\u0449\u0438\u0439 \u0431\u0430\u043b\u0430\u043d\u0441", None))
        self.balance_lbl.setText(QCoreApplication.translate("MainWindow", u"1000", None))
        self.income_icon.setText("")
        self.income_lbl.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0445\u043e\u0434", None))
        self.income_balance_lbl.setText(QCoreApplication.translate("MainWindow", u"1000", None))
        self.outcome_icon.setText("")
        self.outcome_lbl.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0442\u0440\u0430\u0442\u044b", None))
        self.outcome_balance_lbl.setText(QCoreApplication.translate("MainWindow", u"1000", None))
        self.category_title_lbl.setText(QCoreApplication.translate("MainWindow", u"\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438", None))
        self.category_edit_btn.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.new_btn.setText(QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u0430\u044f \u043e\u043f\u0435\u0440\u0430\u0446\u0438\u044f", None))
        self.edit_btn.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u043e\u043f\u0435\u0440\u0430\u0446\u0438\u044e", None))
        self.delete_btn.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u043e\u043f\u0435\u0440\u0430\u0446\u0438\u044e", None))
    # retranslateUi

