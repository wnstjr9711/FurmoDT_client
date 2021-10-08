from PySide2.QtWidgets import QDialog
from ui_login import Ui_Dialog


class LoginWindow(QDialog, Ui_Dialog):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.setupUi(self)
