# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_loginApghyV.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(360, 540)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-radius: 10px;")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.pushButton = QPushButton(self.frame)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setStyleSheet(u"background-color: rgb(85, 255, 255);")

        self.gridLayout_2.addWidget(self.pushButton, 1, 0, 1, 1)

        self.widget = QWidget(self.frame)
        self.widget.setObjectName(u"widget")
        self.widget.setStyleSheet(u"background-color: rgb(85, 255, 255);")
        self.gridLayout_3 = QGridLayout(self.widget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.user_id = QLineEdit(self.widget)
        self.user_id.setObjectName(u"user_id")
        self.user_id.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.user_id, 0, 0, 1, 1)

        self.user_password = QLineEdit(self.widget)
        self.user_password.setObjectName(u"user_password")
        self.user_password.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.user_password, 1, 0, 1, 1)


        self.gridLayout_2.addWidget(self.widget, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"\n"
"\ub85c\uadf8\uc778\n"
"", None))
        self.user_id.setText(QCoreApplication.translate("Dialog", u"id", None))
        self.user_password.setText(QCoreApplication.translate("Dialog", u"password", None))
    # retranslateUi

