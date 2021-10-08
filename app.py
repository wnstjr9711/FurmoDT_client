from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtGui import QIcon
from app_setting import AdvancedSetup
import socket_client
import qasync
import sys
import os


class MainWindow(QMainWindow):
    def __init__(self, client_id):
        super(MainWindow, self).__init__()
        self.main = AdvancedSetup(self)
        self.main.client['id'] = client_id
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        if self.main.work_widget.isVisible():
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
        self.main.event_work_add_subtitle(e.mimeData().urls()[0].toLocalFile())


app = QApplication(sys.argv)
app.setStyle('Fusion')
app.setWindowIcon(QIcon(os.path.join('files', 'furmodt-favicon.ico')))
window = MainWindow('wnstjr')
window.show()

loop = qasync.QEventLoop(app)
loop.create_task(socket_client.conn(window.main))
loop.run_forever()
