from PySide2.QtWidgets import QApplication, QMainWindow
from ui_setup import AdvancedSetup
import qasync
import socket_client
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.main = AdvancedSetup(self)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        e.accept()

    def dragMoveEvent(self, e):
        target = self.main.work_widget
        x_range = range(*(target.x(), target.x() + target.width() + 1))
        y_range = range(*(target.y(), target.y() + target.height() + 1))
        if e.pos().x() in x_range and e.pos().y() in y_range:
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.main.add_subtitle(e.mimeData().urls()[0].toLocalFile())


app = QApplication(sys.argv)
app.setStyle('Fusion')
window = MainWindow()
window.show()

loop = qasync.QEventLoop(app)
loop.create_task(socket_client.conn(window.main))
loop.run_forever()
