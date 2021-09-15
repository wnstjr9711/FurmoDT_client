from PySide2.QtWidgets import QApplication, QMainWindow
from ui_setup import AdvancedSetup
import qasync
import socket_client
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.main = AdvancedSetup(self)


app = QApplication(sys.argv)
window = MainWindow()
window.show()

loop = qasync.QEventLoop(app)
loop.create_task(socket_client.conn(window.main))
loop.run_forever()
