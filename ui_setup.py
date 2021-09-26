from PySide2 import QtCore
from PySide2.QtCore import QUrl, QTimer, QThread, QSize
from PySide2.QtGui import QFont
from PySide2.QtMultimediaWidgets import QVideoWidget
from PySide2.QtMultimedia import QMediaPlayer, QMediaPlaylist
from PySide2.QtWidgets import QLineEdit, QLabel, QListWidgetItem
from ui_main import Ui_MainWindow
import datetime
import os
import gdown

FOLDER = 'video_download'


class AdvancedSetup(Ui_MainWindow):
    def __init__(self, main):
        super().__init__()
        # ui 불러오기
        self.main = main
        self.setupUi(self.main)
        # 프로젝트 목록
        self.project_list = list()

        # ui 설정
        font = QFont()
        font.setPointSize(20)
        self.project_table.setFont(font)
        # self.project_table.setColumnCount(2)
        # self.project_table.setHorizontalHeaderLabels(['프로젝트 이름', '동영상 이름'])
        # self.project_table.resizeColumnsToContents()

        # 색상 설정
        self.project_table.setStyleSheet("border-radius: 10px;"
                                         "background-color: rgb(255, 255, 255);")

        # 타이머
        self.timer = QTimer()
        self.timer.setInterval(1)  # 1/1000 sec
        self.timer.timeout.connect(self.timeout)

        # 동영상 플레이어
        self.duration = 0
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist(self.player)
        self.video_widget = QVideoWidget(self.videowidget)
        self.video_widget.resize(QtCore.QSize(480, 360))
        self.player.setVideoOutput(self.video_widget)
        # 자막
        self.subtitle = QLabel(self.videowidget)
        x, y = self.video_widget.width(), int(self.video_widget.height()/8)
        self.subtitle.setGeometry(0, self.videowidget.height() - y, x, y)
        self.subtitle.setStyleSheet("background-color: black;"
                                    "color: white;")
        self.subtitle.setAlignment(QtCore.Qt.AlignCenter)
        self.subtitle.setText("test1\ntest2\ntest3")

        # 클라이언트 초기화
        self.client = {
            "id": "",
            "qualified": "",
            "GET": None,     # None: project,  project id: work
            "POST": dict(),
        }

        # 작업 영상 url, name
        self.work_video = None
        self.thread_video_download = None

        # 초기화면 설정
        self.default_view()

        # ********************** 동영상 플레이어 조작 이벤트 ********************** #
        self.play.clicked.connect(self.play_clicked_event)
        self.prev.clicked.connect(self.pass_prev_video)
        self.next.clicked.connect(self.pass_next_video)
        self.stop.clicked.connect(self.stop_video)
        self.soundSlider.valueChanged.connect(self.sound_slider_event)
        self.videoSlider.sliderPressed.connect(self.pause_video)
        self.videoSlider.sliderReleased.connect(self.set_position)
        self.player.durationChanged.connect(self.video_duration_event)
        self.player.positionChanged.connect(self.video_position_event)
        # ********************** 동영상 플레이어 조작 이벤트 ********************** #

        # ********************** 프로젝트 조작 이벤트 ********************** #
        # 생성
        self.button_create_project.clicked.connect(self.create_project)
        self.buttonbox_create.accepted.connect(self.create_accept)
        self.buttonbox_create.rejected.connect(self.create_reject)
        # 입장
        self.project_table.itemDoubleClicked.connect(self.join_project)
        # ********************** 프로젝트 조작 이벤트 ********************** #

        # ********************** 작업 조작 이벤트 ********************** #
        self.quit_work.clicked.connect(self.back_to_project)
        # ********************** 작업 조작 이벤트 ********************** #

    # post 메시지 초기화
    def setdefault_client(self):
        self.client['POST'] = {}

    # ********************** 화면 전환 함수 ********************** #
    def default_view(self):
        self.project_input.setVisible(False)
        self.work_widget.setVisible(False)
        self.main.resize(QSize(1080, 720))

    def project_view(self):
        self.work_widget.setVisible(False)
        self.project_widget.setVisible(True)
        self.project_input.setVisible(False)
        self.project_list.clear()
        self.project_table.clear()
        self.playlist.clear()

    def work_view(self):
        self.project_widget.setVisible(False)
        self.work_widget.setVisible(True)

    def refresh(self, ret):
        # 프로젝트 목록 갱신
        if type(ret) == list:
            self.work_video = None
            add = set(ret).difference(self.project_list)
            for i in sorted(add):
                self.project_list.append(i)
                item = QListWidgetItem(i)
                item.setTextAlignment(QtCore.Qt.AlignHCenter)
                self.project_table.addItem(item)
        # 자막 화면 갱신
        else:
            if self.work_video != ret['metadata']:
                self.work_video = ret['metadata']
                self.set_video()
            # TODO 자막 화면 갱신
    # ********************** 화면 전환 함수 ********************** #

    # 타이머 함수
    def timeout(self):
        self.set_playtime(self.player.position())
        self.videoSlider.setValue(self.player.position())
        # TODO 자막 갱신

    # ********************** 동영상 플레이 이벤트 함수 ********************** #
    def play_video(self):
        self.play.setText('❚❚')
        self.player.play()
        self.timer.start()
        self.play.setShortcut(u"Space")

    def pause_video(self):
        self.play.setText('▶')
        self.player.pause()
        self.timer.stop()
        self.play.setShortcut(u"Space")

    def pass_prev_video(self):
        if self.player.isVideoAvailable():
            target = self.player.position()-5000
            self.videoSlider.setValue(target)
            if self.videoSlider.value() == 0:
                self.stop_video()
            else:
                self.set_position()
                self.play_video()

    def pass_next_video(self):
        if self.player.isVideoAvailable():
            target = self.player.position()+5000
            self.videoSlider.setValue(target)
            self.set_position()
            self.play_video()

    def stop_video(self):
        self.videoSlider.setValue(0)
        self.set_position()
        self.pause_video()

    def set_playtime(self, start):
        start = str(datetime.timedelta(milliseconds=start))[:10]
        end = str(datetime.timedelta(milliseconds=self.duration))[:10]
        self.playtime.setText('{} / {}'.format(start, end))

    def play_clicked_event(self):
        if self.play.text() == '❚❚':
            self.pause_video()
        else:
            if self.player.isVideoAvailable():
                self.play_video()

    def sound_slider_event(self):
        self.player.setVolume(self.soundSlider.value())
        self.sound.setText(str(self.soundSlider.value()))

    def video_duration_event(self):
        self.duration = self.player.duration()
        self.videoSlider.setMaximum(self.duration)
        self.set_playtime(0)

    def video_position_event(self):
        if self.player.position() == self.duration:
            self.stop_video()

    def set_position(self):
        self.player.setPosition(self.videoSlider.value())
        self.set_playtime(self.videoSlider.value())

    def set_video(self):
        filename = self.work_video[1]
        location = os.path.join(os.getcwd(), FOLDER)
        video_path = os.path.join(location, filename)
        if not os.path.exists(video_path):
            self.load_video_event(location, video_path, self.work_video[0].split('/')[-2])
        else:
            self.playlist.clear()
            self.playlist.addMedia(QUrl(FOLDER + '/' + filename))
            self.player.setPlaylist(self.playlist)
            self.play_video()

    def load_video_event(self, location, video_path, fileid):
        if not os.path.exists(location):
            os.mkdir(location)
        self.thread_video_download = DownLoadThread(self, 'https://drive.google.com/uc?id=' + fileid, video_path)
        self.thread_video_download.start()

    # ********************** 동영상 플레이 이벤트 함수 ********************** #

    # ********************** 프로젝트 이벤트 함수 ********************** #
    def create_project(self):
        self.project_input.setVisible(True)

    def create_accept(self):
        self.project_input.setVisible(False)
        project = list(filter(lambda x: type(x) == QLineEdit, self.project_input.children()))
        pid, fid = map(lambda x: x.text(), project)
        self.client['POST'][1] = [pid, fid, gdown.getfilename(fid)]
        clear = list(map(lambda x: x.clear(), project))
        # TODO // URL 검증 및 에러 체크 구문

    def create_reject(self):
        self.project_input.setVisible(False)

    def join_project(self):
        self.client['GET'] = self.project_table.currentItem().text()
        self.work_view()
    # ********************** 프로젝트 이벤트 함수 ********************** #

    # ********************** 작업 이벤트 함수 ********************** #
    def back_to_project(self):
        self.client['GET'] = None
        self.project_view()
    # ********************** 작업 이벤트 함수 ********************** #


# ********************** 쓰레드 작업 ********************** #
class DownLoadThread(QThread):
    def __init__(self, main, download_link, video_path):
        super(DownLoadThread, self).__init__()
        self.main = main
        self.download_link = download_link
        self.video_path = video_path
        self.bar = self.main.load_video

    def run(self):
        gdown.download(self.download_link, self.video_path, self.bar)
        self.main.set_video()
# ********************** 쓰레드 작업 ********************** #

# TODO // 자막 확인, 작업 시트 만들기
