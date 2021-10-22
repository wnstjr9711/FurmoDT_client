from PySide2.QtCore import Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QDialog
from ui_login import Ui_Dialog
import requests
import config


class LoginWindow(QDialog, Ui_Dialog):
    def __init__(self, display_size):
        super(LoginWindow, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowFlags())

        self.authorized = None
        self.pushButton.clicked.connect(self.login)
        x, y = display_size.width(), display_size.height()
        self.resize(x/8, y/4)
        self.font = QFont("Nanum Myeongjo", int(self.pushButton.height() * 0.8))
        self.user_id.setFont(self.font)
        self.user_password.setFont(self.font)
        self.pushButton.setFont(self.font)
        self.exec_()

    def login(self):
        req = requests.post(f'{config.PREFIX}://{config.SERVER}/login', params={'user_id': self.user_id.text(),
                                                                                'user_pw': self.user_password.text()})
        if req.ok:
            msg, auth_level = req.json().values()
            if auth_level:
                self.authorized = self.user_id.text(), auth_level
                self.close()
            else:
                print(msg)
