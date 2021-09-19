from PySide2 import QtCore
from PySide2.QtCore import QUrl, QTimer
from PySide2.QtGui import QFont
from PySide2.QtMultimediaWidgets import QVideoWidget
from PySide2.QtMultimedia import QMediaPlayer, QMediaPlaylist
from PySide2.QtWidgets import QFileDialog, QLineEdit, QTableWidgetItem
from ui_main import Ui_MainWindow
import datetime
import os
import gdown


class AdvancedSetup(Ui_MainWindow):
    def __init__(self, main):
        super().__init__()
        # ui 불러오기
        self.setupUi(main)

        # 초기화면 설정
        self.default_view()

        # ui 설정
        font = QFont()
        font.setPointSize(15)
        self.project_table.setFont(font)
        # self.project_table.setColumnCount(2)
        # self.project_table.setHorizontalHeaderLabels(['프로젝트 이름', '동영상 이름'])
        # self.project_table.resizeColumnsToContents()

        # 색상 설정
        self.project_table.setStyleSheet("border-radius: 10px;"
                                         "background-color: rgb(255, 255, 255);")
        self.work_table.setStyleSheet("border-radius: 10px;"
                                      "background-color: rgb(255, 255, 255);")

        # 타이머
        self.sec = 0
        self.timer = QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.timeout)

        # 동영상 플레이어
        self.duration = 0
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist(self.player)
        self.video_widget = QVideoWidget(self.videowidget)
        self.video_widget.resize(QtCore.QSize(480, 360))
        self.player.setVideoOutput(self.video_widget)

        # 클라이언트 초기화
        self.client = {
            "id": "",
            "qualified": "",
            "create_project": list(),
            "get_project_work": None,     # None: project,  project id: work
        }

        # ********************** 동영상 플레이어 조작 이벤트 ********************** #
        self.play.clicked.connect(self.play_clicked_event)
        self.prev.clicked.connect(self.pass_prev_video)
        self.next.clicked.connect(self.pass_next_video)
        self.stop.clicked.connect(self.stop_video)
        self.soundSlider.valueChanged.connect(self.sound_slider_event)
        self.videoSlider.sliderPressed.connect(self.video_slider_pressed_event)
        self.videoSlider.sliderReleased.connect(self.video_slider_released_event)
        self.player.durationChanged.connect(self.video_duration_event)
        self.player.positionChanged.connect(self.video_position_event)
        # ********************** 동영상 플레이어 조작 이벤트 ********************** #

        # 프로젝트 목록
        self.project_list = list()
        # 작업 영상 url, name
        self.work_video = None

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
        self.load_video.clicked.connect(self.load_video_event)
        # ********************** 작업 조작 이벤트 ********************** #

    # ********************** 화면 전환 함수 ********************** #
    def default_view(self):
        self.project_widget.setVisible(True)
        self.project_input.setVisible(False)
        self.work_widget.setVisible(False)

    def work_view(self):
        self.project_widget.setVisible(False)
        self.work_widget.setVisible(True)

    def refresh(self, ret):
        # 프로젝트 목록 갱신
        if type(ret) == list:
            add = set(ret).difference(self.project_list)
            for i in sorted(add):
                self.project_list.append(i)
                self.project_table.addItem(i)

        # 자막 화면 갱신
        else:
            if self.work_video != ret['metadata']:
                self.work_video = ret['metadata']
    # ********************** 화면 전환 함수 ********************** #

    # 타이머 함수
    def timeout(self):
        self.sec += 1
        self.set_playtime(self.player.position() + self.sec)
        self.videoSlider.setValue(self.player.position())

    # ********************** 동영상 플레이 이벤트 함수 ********************** #
    def play_video(self):
        self.play.setText('❚❚')
        self.player.play()
        self.sec = 0
        self.timer.start()
        self.play.setShortcut(u"Space")

    def pause_video(self):
        self.play.setText('▶')
        self.player.pause()
        self.timer.stop()
        self.play.setShortcut(u"Space")

    def pass_prev_video(self):
        if self.player.isVideoAvailable():
            self.video_slider_pressed_event()
            target = self.player.position()-5000
            self.videoSlider.setValue(target)
            if self.videoSlider.value() == 0:
                self.stop_video()
            else:
                self.video_slider_released_event()
                self.play_video()

    def pass_next_video(self):
        if self.player.isVideoAvailable():
            self.video_slider_pressed_event()
            target = self.player.position()+5000
            self.videoSlider.setValue(target)
            self.video_slider_released_event()
            self.play_video()

    def stop_video(self):
        self.video_slider_pressed_event()
        self.videoSlider.setValue(0)
        self.video_slider_released_event()

    def set_playtime(self, start):
        start = str(datetime.timedelta(milliseconds=start))[:10]
        end = str(datetime.timedelta(milliseconds=self.duration))[:10]
        if start >= end:
            start = end
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
        self.sec = 0
        if self.player.position() == self.duration:
            self.stop_video()

    def video_slider_pressed_event(self):
        self.pause_video()

    def video_slider_released_event(self):
        self.player.setPosition(self.videoSlider.value())
        self.set_playtime(self.videoSlider.value())
    # ********************** 동영상 플레이 이벤트 함수 ********************** #

    # ********************** 프로젝트 이벤트 함수 ********************** #
    def create_project(self):
        self.project_input.setVisible(True)

    def create_accept(self):
        self.project_input.setVisible(False)
        for i in self.project_input.children():
            if type(i) == QLineEdit and i.text():
                self.client['create_project'].append(i.text())
                i.clear()
        # TODO // 에러 체크 구문
        if len(self.client['create_project']) != 2:
            self.client['create_project'].clear()

    def create_reject(self):
        self.project_input.setVisible(False)

    def join_project(self):
        self.client['get_project_work'] = self.project_table.currentItem().text()
        self.work_view()
    # ********************** 프로젝트 이벤트 함수 ********************** #

    # ********************** 작업 이벤트 함수 ********************** #
    def back_to_project(self):
        self.client['get_project_work'] = None
        self.default_view()

    def load_video_event(self):
        fileid, filename = self.work_video[0].split('/')[-2], self.work_video[1]
        location = os.path.join(os.getcwd(), 'video_download')
        if not os.path.exists(location):
            os.mkdir(location)
        video_path = os.path.join(location, filename)
        download_link = 'https://drive.google.com/uc?id=' + fileid
        # download_link = 'https://drive.google.com/uc?id=' + '1qNGOzi_PgHNaM056GeZlD6dKeg3JjmWo'
        gdown.download(download_link, video_path)

        self.playlist.clear()
        self.playlist.addMedia(QUrl(video_path))
        self.player.setPlaylist(self.playlist)
    # ********************** 작업 이벤트 함수 ********************** #


# TODO // 동영상 업로드 확인(loadvideoevent) 내일 할일 작업 시트 만들기
