from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QIcon
import qasync
import sys
import os
import socket_client
from mainwindow import MainWindow
from login import LoginWindow

app = QApplication(sys.argv)
app.setStyle('Fusion')
app.setWindowIcon(QIcon(os.path.join('files', 'furmodt-favicon.ico')))

display_size = app.primaryScreen().size()
client = LoginWindow(display_size)

if client.authorized:
    window = MainWindow(*client.authorized)
    window.show()
    window.resize(display_size.width()/2, display_size.height()/2)

    loop = qasync.QEventLoop(app)
    loop.create_task(socket_client.conn(window))
    loop.run_forever()
