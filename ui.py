# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'applicationMrOYjS.ui'
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
        MainWindow.resize(1080, 720)
        self.action = QAction(MainWindow)
        self.action.setObjectName(u"action")
        self.action_2 = QAction(MainWindow)
        self.action_2.setObjectName(u"action_2")
        self.action_3 = QAction(MainWindow)
        self.action_3.setObjectName(u"action_3")
        self.openvideo = QAction(MainWindow)
        self.openvideo.setObjectName(u"openvideo")
        self.action_5 = QAction(MainWindow)
        self.action_5.setObjectName(u"action_5")
        self.action_6 = QAction(MainWindow)
        self.action_6.setObjectName(u"action_6")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.widget_2 = QWidget(self.centralwidget)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMinimumSize(QSize(500, 500))
        self.verticalLayout = QVBoxLayout(self.widget_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.videowidget = QWidget(self.widget_2)
        self.videowidget.setObjectName(u"videowidget")
        self.videowidget.setMinimumSize(QSize(480, 360))

        self.verticalLayout.addWidget(self.videowidget)

        self.widget_5 = QWidget(self.widget_2)
        self.widget_5.setObjectName(u"widget_5")
        self.verticalLayout_2 = QVBoxLayout(self.widget_5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.videoSlider = QSlider(self.widget_5)
        self.videoSlider.setObjectName(u"videoSlider")
        self.videoSlider.setMaximum(0)
        self.videoSlider.setOrientation(Qt.Horizontal)

        self.verticalLayout_2.addWidget(self.videoSlider)

        self.playtime = QLabel(self.widget_5)
        self.playtime.setObjectName(u"playtime")
        self.playtime.setLayoutDirection(Qt.LeftToRight)
        self.playtime.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_2.addWidget(self.playtime)


        self.verticalLayout.addWidget(self.widget_5)

        self.widget_3 = QWidget(self.widget_2)
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
        self.soundSlider.setMaximum(100)
        self.soundSlider.setValue(100)
        self.soundSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_2.addWidget(self.soundSlider)


        self.verticalLayout.addWidget(self.widget_3)

        self.widget_4 = QWidget(self.widget_2)
        self.widget_4.setObjectName(u"widget_4")

        self.verticalLayout.addWidget(self.widget_4)


        self.gridLayout_2.addWidget(self.widget_2, 0, 0, 1, 1)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.projects = QTableView(self.widget)
        self.projects.setObjectName(u"projects")

        self.gridLayout.addWidget(self.projects, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.widget, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1080, 21))
        self.menuasd = QMenu(self.menubar)
        self.menuasd.setObjectName(u"menuasd")
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menu_2 = QMenu(self.menubar)
        self.menu_2.setObjectName(u"menu_2")
        self.menu_3 = QMenu(self.menubar)
        self.menu_3.setObjectName(u"menu_3")
        self.menu_4 = QMenu(self.menubar)
        self.menu_4.setObjectName(u"menu_4")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuasd.menuAction())
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())
        self.menuasd.addAction(self.openvideo)
        self.menu.addSeparator()
        self.menu.addAction(self.action_5)
        self.menu.addAction(self.action_6)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"FurmoDT", None))
        self.action.setText(QCoreApplication.translate("MainWindow", u"\uc5f4\uae30", None))
        self.action_2.setText(QCoreApplication.translate("MainWindow", u"\uc800\uc7a5", None))
#if QT_CONFIG(shortcut)
        self.action_2.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.action_3.setText(QCoreApplication.translate("MainWindow", u"\ub2e4\ub978\uc774\ub984\uc73c\ub85c\uc800\uc7a5", None))
        self.openvideo.setText(QCoreApplication.translate("MainWindow", u"\ub3d9\uc601\uc0c1 \uc5f4\uae30", None))
#if QT_CONFIG(shortcut)
        self.openvideo.setShortcut(QCoreApplication.translate("MainWindow", u"Alt+O", None))
#endif // QT_CONFIG(shortcut)
        self.action_5.setText(QCoreApplication.translate("MainWindow", u"\uc2e4\ud589 \ucde8\uc18c", None))
#if QT_CONFIG(shortcut)
        self.action_5.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Z", None))
#endif // QT_CONFIG(shortcut)
        self.action_6.setText(QCoreApplication.translate("MainWindow", u"\ub2e4\uc2dc \uc2e4\ud589", None))
#if QT_CONFIG(shortcut)
        self.action_6.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+Z", None))
#endif // QT_CONFIG(shortcut)
        self.playtime.setText(QCoreApplication.translate("MainWindow", u"0:00:00 / 0:00:00", None))
        self.play.setText(QCoreApplication.translate("MainWindow", u"\u25b6", None))
        self.prev.setText(QCoreApplication.translate("MainWindow", u" \u25c0\u25c0", None))
        self.next.setText(QCoreApplication.translate("MainWindow", u"\u25b6\u25b6", None))
        self.stop.setText(QCoreApplication.translate("MainWindow", u"\u25a0", None))
        self.sound.setText(QCoreApplication.translate("MainWindow", u"100", None))
        self.menuasd.setTitle(QCoreApplication.translate("MainWindow", u"\ud30c\uc77c", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\ud3b8\uc9d1", None))
        self.menu_2.setTitle(QCoreApplication.translate("MainWindow", u"\uc790\ub9c9", None))
        self.menu_3.setTitle(QCoreApplication.translate("MainWindow", u"\uc140\ud3b8\uc9d1", None))
        self.menu_4.setTitle(QCoreApplication.translate("MainWindow", u"\ubd80\uac00\uc791\uc5c5", None))
    # retranslateUi

