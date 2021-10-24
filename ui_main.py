# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_mainawstWs.ui'
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
        MainWindow.resize(1303, 768)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.playerwidget = QWidget(self.centralwidget)
        self.playerwidget.setObjectName(u"playerwidget")
        self.playerwidget.setMinimumSize(QSize(528, 500))
        self.playerwidget.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(self.playerwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.videowidget = QWidget(self.playerwidget)
        self.videowidget.setObjectName(u"videowidget")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.videowidget.sizePolicy().hasHeightForWidth())
        self.videowidget.setSizePolicy(sizePolicy)
        self.videowidget.setMinimumSize(QSize(480, 360))
        self.videowidget.setMaximumSize(QSize(16777215, 16777215))
        self.videowidget.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.gridLayout = QGridLayout(self.videowidget)
        self.gridLayout.setObjectName(u"gridLayout")

        self.verticalLayout.addWidget(self.videowidget)

        self.widget_5 = QWidget(self.playerwidget)
        self.widget_5.setObjectName(u"widget_5")
        self.widget_5.setMinimumSize(QSize(510, 0))
        self.widget_5.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.widget_5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.videoSlider = QSlider(self.widget_5)
        self.videoSlider.setObjectName(u"videoSlider")
        self.videoSlider.setMaximumSize(QSize(16777215, 16777215))
        self.videoSlider.setMaximum(0)
        self.videoSlider.setOrientation(Qt.Horizontal)

        self.verticalLayout_2.addWidget(self.videoSlider)

        self.playtime = QLabel(self.widget_5)
        self.playtime.setObjectName(u"playtime")
        self.playtime.setLayoutDirection(Qt.LeftToRight)
        self.playtime.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_2.addWidget(self.playtime)


        self.verticalLayout.addWidget(self.widget_5)

        self.widget_3 = QWidget(self.playerwidget)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.button_play = QPushButton(self.widget_3)
        self.button_play.setObjectName(u"button_play")

        self.horizontalLayout_2.addWidget(self.button_play)

        self.button_prev = QPushButton(self.widget_3)
        self.button_prev.setObjectName(u"button_prev")

        self.horizontalLayout_2.addWidget(self.button_prev)

        self.button_next = QPushButton(self.widget_3)
        self.button_next.setObjectName(u"button_next")

        self.horizontalLayout_2.addWidget(self.button_next)

        self.button_stop = QPushButton(self.widget_3)
        self.button_stop.setObjectName(u"button_stop")

        self.horizontalLayout_2.addWidget(self.button_stop)

        self.sound = QLabel(self.widget_3)
        self.sound.setObjectName(u"sound")
        self.sound.setMinimumSize(QSize(18, 0))

        self.horizontalLayout_2.addWidget(self.sound)

        self.soundSlider = QSlider(self.widget_3)
        self.soundSlider.setObjectName(u"soundSlider")
        self.soundSlider.setMinimumSize(QSize(100, 0))
        self.soundSlider.setMaximumSize(QSize(144, 22))
        self.soundSlider.setMaximum(100)
        self.soundSlider.setValue(100)
        self.soundSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_2.addWidget(self.soundSlider)


        self.verticalLayout.addWidget(self.widget_3)


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
        self.project_input.setMaximumSize(QSize(16777215, 16777215))
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

        self.table_project = QListWidget(self.project_widget)
        self.table_project.setObjectName(u"table_project")

        self.verticalLayout_5.addWidget(self.table_project)


        self.gridLayout_2.addWidget(self.project_widget, 0, 1, 1, 1)

        self.work_widget = QWidget(self.centralwidget)
        self.work_widget.setObjectName(u"work_widget")
        self.gridLayout_3 = QGridLayout(self.work_widget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.table_work = QTableWidget(self.work_widget)
        if (self.table_work.columnCount() < 3):
            self.table_work.setColumnCount(3)
        if (self.table_work.rowCount() < 200):
            self.table_work.setRowCount(200)
        self.table_work.setObjectName(u"table_work")
        self.table_work.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table_work.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table_work.setAutoScroll(True)
        self.table_work.setRowCount(200)
        self.table_work.setColumnCount(3)
        self.table_work.horizontalHeader().setVisible(True)
        self.table_work.horizontalHeader().setCascadingSectionResizes(False)
        self.table_work.horizontalHeader().setProperty("showSortIndicator", False)
        self.table_work.horizontalHeader().setStretchLastSection(False)
        self.table_work.verticalHeader().setVisible(True)
        self.table_work.verticalHeader().setCascadingSectionResizes(False)
        self.table_work.verticalHeader().setProperty("showSortIndicator", False)

        self.gridLayout_3.addWidget(self.table_work, 3, 0, 1, 1)

        self.widget = QWidget(self.work_widget)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.button_work_quit = QPushButton(self.widget)
        self.button_work_quit.setObjectName(u"button_work_quit")

        self.horizontalLayout.addWidget(self.button_work_quit)

        self.button_add_language = QPushButton(self.widget)
        self.button_add_language.setObjectName(u"button_add_language")
        self.button_add_language.setEnabled(True)

        self.horizontalLayout.addWidget(self.button_add_language)

        self.button_delete_language = QPushButton(self.widget)
        self.button_delete_language.setObjectName(u"button_delete_language")

        self.horizontalLayout.addWidget(self.button_delete_language)

        self.button_work_save = QPushButton(self.widget)
        self.button_work_save.setObjectName(u"button_work_save")

        self.horizontalLayout.addWidget(self.button_work_save)

        self.pushButton_2 = QPushButton(self.widget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setEnabled(False)

        self.horizontalLayout.addWidget(self.pushButton_2)


        self.gridLayout_3.addWidget(self.widget, 0, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.button_tc_set = QPushButton(self.work_widget)
        self.button_tc_set.setObjectName(u"button_tc_set")

        self.horizontalLayout_4.addWidget(self.button_tc_set)

        self.button_tc_in = QPushButton(self.work_widget)
        self.button_tc_in.setObjectName(u"button_tc_in")

        self.horizontalLayout_4.addWidget(self.button_tc_in)

        self.button_tc_out = QPushButton(self.work_widget)
        self.button_tc_out.setObjectName(u"button_tc_out")

        self.horizontalLayout_4.addWidget(self.button_tc_out)


        self.gridLayout_3.addLayout(self.horizontalLayout_4, 2, 0, 1, 1)

        self.workers = QLabel(self.work_widget)
        self.workers.setObjectName(u"workers")
        self.workers.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.workers, 1, 0, 1, 1)


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
        self.playtime.setText(QCoreApplication.translate("MainWindow", u"0:00:00 / 0:00:00", None))
        self.button_play.setText(QCoreApplication.translate("MainWindow", u"\u25b6", None))
#if QT_CONFIG(shortcut)
        self.button_play.setShortcut(QCoreApplication.translate("MainWindow", u"Space", None))
#endif // QT_CONFIG(shortcut)
        self.button_prev.setText(QCoreApplication.translate("MainWindow", u" \u25c0\u25c0", None))
#if QT_CONFIG(shortcut)
        self.button_prev.setShortcut(QCoreApplication.translate("MainWindow", u"F4", None))
#endif // QT_CONFIG(shortcut)
        self.button_next.setText(QCoreApplication.translate("MainWindow", u"\u25b6\u25b6", None))
#if QT_CONFIG(shortcut)
        self.button_next.setShortcut(QCoreApplication.translate("MainWindow", u"F5", None))
#endif // QT_CONFIG(shortcut)
        self.button_stop.setText(QCoreApplication.translate("MainWindow", u"\u25a0", None))
        self.sound.setText(QCoreApplication.translate("MainWindow", u"100", None))
        self.button_create_project.setText(QCoreApplication.translate("MainWindow", u"\ud504\ub85c\uc81d\ud2b8 \uc0dd\uc131", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\ud504\ub85c\uc81d\ud2b8 \uc774\ub984", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\ube44\ub514\uc624 \uc8fc\uc18c", None))
        self.button_work_quit.setText(QCoreApplication.translate("MainWindow", u"\ub098\uac00\uae30", None))
        self.button_add_language.setText(QCoreApplication.translate("MainWindow", u"\uc5b8\uc5b4 \ucd94\uac00\ud558\uae30", None))
        self.button_delete_language.setText(QCoreApplication.translate("MainWindow", u"\uc5b8\uc5b4 \uc0ad\uc81c\ud558\uae30", None))
        self.button_work_save.setText(QCoreApplication.translate("MainWindow", u"\uc790\ub9c9 \ub0b4\ubcf4\ub0b4\uae30", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\ud504\ub85c\uc81d\ud2b8 \uc885\ub8cc", None))
        self.button_tc_set.setText(QCoreApplication.translate("MainWindow", u"TC SET", None))
#if QT_CONFIG(shortcut)
        self.button_tc_set.setShortcut(QCoreApplication.translate("MainWindow", u"F1", None))
#endif // QT_CONFIG(shortcut)
        self.button_tc_in.setText(QCoreApplication.translate("MainWindow", u"TC IN", None))
#if QT_CONFIG(shortcut)
        self.button_tc_in.setShortcut(QCoreApplication.translate("MainWindow", u"F2", None))
#endif // QT_CONFIG(shortcut)
        self.button_tc_out.setText(QCoreApplication.translate("MainWindow", u"TC OUT", None))
#if QT_CONFIG(shortcut)
        self.button_tc_out.setShortcut(QCoreApplication.translate("MainWindow", u"F3", None))
#endif // QT_CONFIG(shortcut)
        self.workers.setText(QCoreApplication.translate("MainWindow", u"\ucc38\uc5ec\uc790", None))
    # retranslateUi

