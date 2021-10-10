import os
import sys

import qasync
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication

from mainwindow import MainWindow
from src import socket_client


app = QApplication(sys.argv)
app.setStyle('Fusion')
app.setWindowIcon(QIcon(os.path.join('files', 'furmodt-favicon.ico')))
window = MainWindow('wnstjr')
window.show()

loop = qasync.QEventLoop(app)
loop.create_task(socket_client.conn(window))
loop.run_forever()
