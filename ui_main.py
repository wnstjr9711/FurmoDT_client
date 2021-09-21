# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'applicationJtxKCZ.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1186, 663)
        icon = QIcon()
        icon.addFile(u"files/furmodt-favicon.ico", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.playerwidget = QWidget(self.centralwidget)
        self.playerwidget.setObjectName(u"playerwidget")
        self.playerwidget.setMinimumSize(QSize(528, 500))
        self.playerwidget.setMaximumSize(QSize(528, 16777215))
        self.verticalLayout = QVBoxLayout(self.playerwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.videowidget = QWidget(self.playerwidget)
        self.videowidget.setObjectName(u"videowidget")
        self.videowidget.setMinimumSize(QSize(480, 360))
        self.videowidget.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.subtitle = QLabel(self.videowidget)
        self.subtitle.setObjectName(u"subtitle")
        self.subtitle.setGeometry(QRect(5, 310, 471, 41))
        self.subtitle.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font: 9pt \"\ub9d1\uc740 \uace0\ub515\";")
        self.subtitle.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.videowidget, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.widget_5 = QWidget(self.playerwidget)
        self.widget_5.setObjectName(u"widget_5")
        self.widget_5.setMinimumSize(QSize(510, 0))
        self.widget_5.setMaximumSize(QSize(510, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.widget_5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.videoSlider = QSlider(self.widget_5)
        self.videoSlider.setObjectName(u"videoSlider")
        self.videoSlider.setMaximumSize(QSize(492, 16777215))
        self.videoSlider.setMaximum(0)
        self.videoSlider.setOrientation(Qt.Horizontal)

        self.verticalLayout_2.addWidget(self.videoSlider)

        self.playtime = QLabel(self.widget_5)
        self.playtime.setObjectName(u"playtime")
        self.playtime.setLayoutDirection(Qt.LeftToRight)
        self.playtime.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_2.addWidget(self.playtime)


        self.verticalLayout.addWidget(self.widget_5, 0, Qt.AlignHCenter)

        self.widget_3 = QWidget(self.playerwidget)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.play = QPushButton(self.widget_3)
        self.play.setObjectName(u"play")

        self.horizontalLayout_2.addWidget(self.play)

        self.prev = QPushButton(self.widget_3)
        self.prev.setObjectName(u"prev")

        self.horizontalLayout_2.addWidget(self.prev)

        self.next = QPushButton(self.widget_3)
        self.next.setObjectName(u"next")

        self.horizontalLayout_2.addWidget(self.next)

        self.stop = QPushButton(self.widget_3)
        self.stop.setObjectName(u"stop")

        self.horizontalLayout_2.addWidget(self.stop)

        self.sound = QLabel(self.widget_3)
        self.sound.setObjectName(u"sound")

        self.horizontalLayout_2.addWidget(self.sound)

        self.soundSlider = QSlider(self.widget_3)
        self.soundSlider.setObjectName(u"soundSlider")
        self.soundSlider.setMinimumSize(QSize(100, 0))
        self.soundSlider.setMaximumSize(QSize(144, 22))
        self.soundSlider.setMaximum(100)
        self.soundSlider.setValue(100)
        self.soundSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_2.addWidget(self.soundSlider)


        self.verticalLayout.addWidget(self.widget_3, 0, Qt.AlignHCenter)

        self.widget_4 = QWidget(self.playerwidget)
        self.widget_4.setObjectName(u"widget_4")

        self.verticalLayout.addWidget(self.widget_4)


        self.gridLayout_2.addWidget(self.playerwidget, 0, 0, 1, 1)

        self.project_widget = QWidget(self.centralwidget)
        self.project_widget.setObjectName(u"project_widget")
        self.project_widget.setMinimumSize(QSize(274, 0))
        self.verticalLayout_5 = QVBoxLayout(self.project_widget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.button_create_project = QPushButton(self.project_widget)
        self.button_create_project.setObjectName(u"button_create_project")
        self.button_create_project.setMinimumSize(QSize(256, 0))
        self.button_create_project.setMaximumSize(QSize(256, 16777215))

        self.verticalLayout_5.addWidget(self.button_create_project, 0, Qt.AlignHCenter)

        self.project_input = QWidget(self.project_widget)
        self.project_input.setObjectName(u"project_input")
        self.project_input.setMaximumSize(QSize(256, 16777215))
        self.formLayout = QFormLayout(self.project_input)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.project_input)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.project_name = QLineEdit(self.project_input)
        self.project_name.setObjectName(u"project_name")
        self.project_name.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.project_name)

        self.label_2 = QLabel(self.project_input)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.video_url = QLineEdit(self.project_input)
        self.video_url.setObjectName(u"video_url")
        self.video_url.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.video_url)

        self.buttonbox_create = QDialogButtonBox(self.project_input)
        self.buttonbox_create.setObjectName(u"buttonbox_create")
        self.buttonbox_create.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.buttonbox_create)


        self.verticalLayout_5.addWidget(self.project_input, 0, Qt.AlignHCenter)

        self.project_table = QListWidget(self.project_widget)
        self.project_table.setObjectName(u"project_table")

        self.verticalLayout_5.addWidget(self.project_table)


        self.gridLayout_2.addWidget(self.project_widget, 0, 1, 1, 1)

        self.work_widget = QWidget(self.centralwidget)
        self.work_widget.setObjectName(u"work_widget")
        self.gridLayout_3 = QGridLayout(self.work_widget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.widget = QWidget(self.work_widget)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.quit_work = QPushButton(self.widget)
        self.quit_work.setObjectName(u"quit_work")

        self.horizontalLayout.addWidget(self.quit_work)

        self.load_video = QPushButton(self.widget)
        self.load_video.setObjectName(u"load_video")

        self.horizontalLayout.addWidget(self.load_video)

        self.pushButton_4 = QPushButton(self.widget)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout.addWidget(self.pushButton_4)

        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)


        self.gridLayout_3.addWidget(self.widget, 0, 0, 1, 1)

        self.work_table = QTableWidget(self.work_widget)
        self.work_table.setObjectName(u"work_table")

        self.gridLayout_3.addWidget(self.work_table, 1, 0, 1, 1)


        self.gridLayout_2.addWidget(self.work_widget, 0, 2, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"FurmoDT", None))
        self.subtitle.setText(QCoreApplication.translate("MainWindow", u"subtitle", None))
        self.playtime.setText(QCoreApplication.translate("MainWindow", u"0:00:00 / 0:00:00", None))
        self.play.setText(QCoreApplication.translate("MainWindow", u"\u25b6", None))
#if QT_CONFIG(shortcut)
        self.play.setShortcut(QCoreApplication.translate("MainWindow", u"Space", None))
#endif // QT_CONFIG(shortcut)
        self.prev.setText(QCoreApplication.translate("MainWindow", u" \u25c0\u25c0", None))
#if QT_CONFIG(shortcut)
        self.prev.setShortcut(QCoreApplication.translate("MainWindow", u"F4", None))
#endif // QT_CONFIG(shortcut)
        self.next.setText(QCoreApplication.translate("MainWindow", u"\u25b6\u25b6", None))
#if QT_CONFIG(shortcut)
        self.next.setShortcut(QCoreApplication.translate("MainWindow", u"F5", None))
#endif // QT_CONFIG(shortcut)
        self.stop.setText(QCoreApplication.translate("MainWindow", u"\u25a0", None))
        self.sound.setText(QCoreApplication.translate("MainWindow", u"100", None))
        self.button_create_project.setText(QCoreApplication.translate("MainWindow", u"\ud504\ub85c\uc81d\ud2b8 \uc0dd\uc131", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\ud504\ub85c\uc81d\ud2b8 \uc774\ub984", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\ube44\ub514\uc624 \uc8fc\uc18c", None))
        self.quit_work.setText(QCoreApplication.translate("MainWindow", u"\ub098\uac00\uae30", None))
        self.load_video.setText(QCoreApplication.translate("MainWindow", u"\ube44\ub514\uc624 \uc5f0\uacb0", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
    # retranslateUi

