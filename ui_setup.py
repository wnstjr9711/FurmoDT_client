from PySide2.QtCore import QUrl, QTimer, QThread, QSize, Qt
from PySide2.QtGui import QFont
from PySide2.QtMultimediaWidgets import QVideoWidget
from PySide2.QtMultimedia import QMediaPlayer, QMediaPlaylist
from PySide2.QtWidgets import QLineEdit, QLabel, QListWidgetItem, QTableWidgetItem, QHeaderView
from ui_main import Ui_MainWindow
import datetime
import pysrt
import gdown
import os
from pandas import read_json

FOLDER = 'video_download'


class AdvancedSetup(Ui_MainWindow):
    def __init__(self, main):
        super().__init__()
        # ui 불러오기
        self.main = main
        self.setupUi(self.main)

        # ui 설정
        font = QFont()
        font.setPointSize(20)
        self.project_table.setFont(font)

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
        self.video_widget.resize(QSize(480, 360))
        self.player.setVideoOutput(self.video_widget)

        # 자막
        self.subtitle = QLabel(self.videowidget)
        x, y = self.video_widget.width(), int(self.video_widget.height()/8)
        self.subtitle.setGeometry(0, self.videowidget.height() - y, x, y)
        self.subtitle.setStyleSheet("background-color: black;"
                                    "color: white;")
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.subtitle.setText("test1\ntest2\ntest3")

        # 프로젝트 목록
        self.project_list = list()

        # 작업 영상 url, name
        self.work_video = dict()
        self.work_header = list()
        self.thread_video_download = None
        self.change = None  # update 주체가 다를 때 변동사항 재전송 방지
        self.work_table.setStyleSheet('QTableWidget QTableCornerButton::section'
                                      '{border-image: url(files/furmodt-favicon.ico);}')

        # 초기화면 설정
        self.default_view()

        # 클라이언트 초기화
        self.client = {
            "id": "",
            "qualified": "",
            "GET": None,     # None: project,  project id: work
            "POST": dict(),
        }

        # ******************************************** 동영상 플레이어 조작 이벤트 ******************************************** #
        self.play.clicked.connect(self.play_clicked_event)
        self.prev.clicked.connect(self.pass_prev_video)
        self.next.clicked.connect(self.pass_next_video)
        self.stop.clicked.connect(self.stop_video)
        self.soundSlider.valueChanged.connect(self.sound_slider_event)
        self.videoSlider.sliderPressed.connect(self.pause_video)
        self.videoSlider.sliderReleased.connect(self.set_position)
        self.player.durationChanged.connect(self.video_duration_event)
        self.player.positionChanged.connect(self.video_position_event)
        # ******************************************** 동영상 플레이어 조작 이벤트 ******************************************** #

        # ******************************************** 프로젝트 조작 이벤트 ******************************************** #
        # 생성
        self.button_create_project.clicked.connect(self.create_project)
        self.buttonbox_create.accepted.connect(self.create_accept)
        self.buttonbox_create.rejected.connect(self.create_reject)
        # 입장
        self.project_table.itemDoubleClicked.connect(self.join_project)
        # ******************************************** 프로젝트 조작 이벤트 ******************************************** #

        # ******************************************** 작업 조작 이벤트 ******************************************** #
        self.quit_work.clicked.connect(self.back_to_project)
        self.add_work.clicked.connect(self.add_language)
        self.work_table.itemChanged.connect(self.update_work)
        # ******************************************** 작업 조작 이벤트 ******************************************** #

    # post 메시지 초기화
    def setdefault_client(self):
        self.client['POST'] = {}

    # 타이머 함수
    def timeout(self):
        self.set_playtime(self.player.position())
        self.videoSlider.setValue(self.player.position())
        # TODO 자막 갱신

    # ******************************************** 화면 전환 함수 ******************************************** #
    def default_view(self):
        for i in range(2):
            self.work_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)
        # 작업 화면 초기화 #
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
                item.setTextAlignment(Qt.AlignHCenter)
                self.project_table.addItem(item)
        # 자막 화면 갱신
        else:
            if 'update' not in ret:  # 전체 갱신
                new_video = ret['metadata']
                new_work_data = read_json(ret['work'])
                new_header = new_work_data.columns.tolist()
                # 프로젝트 확인
                self.work_video = new_video
                self.set_video()
                # header 갱신
                self.work_header = new_header
                self.work_table.setColumnCount(len(new_header))
                self.work_table.setHorizontalHeaderLabels(new_header)
                # 작업 갱신
                for i in range(len(new_work_data.index)):
                    for j in range(len(new_work_data.columns)):
                        target = new_work_data.iloc[i, j]
                        if bool(target):
                            item = QTableWidgetItem(str(target))
                            self.change = (i, j, item.text())
                            self.work_table.setItem(i, j, item)
            else:  # 부분 갱신
                if self.work_header != ret['header']:
                    self.work_header = ret['header']
                    self.work_table.setColumnCount(len(self.work_header))
                    self.work_table.setHorizontalHeaderLabels(self.work_header)
                for update in ret['update']:
                    row, column, text = update
                    if not self.work_table.item(row, column) or self.work_table.item(row, column).text() != text:
                        self.change = update
                        self.work_table.setItem(row, column, QTableWidgetItem(text))
    # ******************************************** 화면 전환 함수 ******************************************** #

    # ******************************************** 동영상 플레이 이벤트 함수 ******************************************** #
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
        start = str(datetime.timedelta(milliseconds=start)).split(':')
        end = str(datetime.timedelta(milliseconds=self.duration)).split(':')
        start_sec, end_sec = start.pop(-1)[:6], end.pop(-1)[:6]
        self.playtime.setText('{}:{}:{} / {}:{}:{}'.format(*start, start_sec, *end, end_sec))

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
        filename = self.work_video['video']
        location = os.path.join(os.getcwd(), FOLDER)
        video_path = os.path.join(location, filename)
        if not os.path.exists(video_path):
            self.load_video_event(location, video_path, self.work_video['url'].split('/')[-2])
        else:
            self.playlist.clear()
            self.playlist.addMedia(QUrl.fromLocalFile(os.path.join(os.getcwd(), FOLDER, filename)))
            self.player.setPlaylist(self.playlist)

    def load_video_event(self, location, video_path, fileid):
        if not os.path.exists(location):
            os.mkdir(location)
        self.thread_video_download = DownLoadThread(self, 'https://drive.google.com/uc?id=' + fileid, video_path)
        self.thread_video_download.start()

    # ******************************************** 동영상 플레이 이벤트 함수 ******************************************** #

    # ******************************************** 프로젝트 이벤트 함수 ******************************************** #
    def create_project(self):
        self.project_input.setVisible(True)

    def create_accept(self):
        self.project_input.setVisible(False)
        project = list(filter(lambda x: type(x) == QLineEdit, self.project_input.children()))
        project_name, file_url = map(lambda x: x.text(), project)
        self.client['POST'][1] = [project_name, file_url, gdown.getfilename(file_url)]
        clear = list(map(lambda x: x.clear(), project))
        # TODO // URL 검증 및 에러 체크 구문

    def create_reject(self):
        self.project_input.setVisible(False)

    def join_project(self):
        self.client['GET'] = self.project_table.currentItem().text()
        self.work_view()
    # ******************************************** 프로젝트 이벤트 함수 ******************************************** #

    # ******************************************** 작업 이벤트 함수 ******************************************** #
    def back_to_project(self):
        self.client['GET'] = None
        self.work_table.clear()
        self.project_view()

    def add_language(self):
        # TODO 언어 선택
        msg, num = '영어', 1
        if msg in self.work_header:
            while '{} ({})'.format(msg, num) in self.work_header:
                num += 1
            msg = '{} ({})'.format(msg, num)
        self.client['POST'][3] = [msg]
        # TODO 언어 선택

    def update_work(self):
        cell = self.work_table.currentItem()
        cur_row = -1
        if self.change:
            cur_row = max(cur_row, self.change[0])
        if cell:
            cell_data = (cell.row(), cell.column(), cell.text())
            if cell_data != self.change:
                self.client['POST'][4] = [cell_data]
                cur_row = max(cur_row, cell.row())
                self.change = None
        if cur_row + 50 >= self.work_table.rowCount():
            self.work_table.setRowCount(self.work_table.rowCount() + 100)

    def add_subtitle(self, url):
        subs = pysrt.open(url)
        srt = list()
        for i in subs:
            srt.append((i.index - 1, 0, str(i.start).replace(',', '.')))
            srt.append((i.index - 1, 1, str(i.end).replace(',', '.')))
            srt.append((i.index - 1, 2, str(i.text)))
        self.client['POST'][4] = srt
    # ******************************************** 작업 이벤트 함수 ******************************************** #


# ******************************************** 쓰레드 작업 ******************************************** #
class DownLoadThread(QThread):
    def __init__(self, main, download_link, video_path):
        super(DownLoadThread, self).__init__()
        self.main = main
        self.download_link = download_link
        self.video_path = video_path
        # TODO 다운로드 진행률 표시
        # self.bar = self.main.load_video
        # gdown 188번째 줄
        # 295번째 줄
        # TODO 다운로드 진행률 표시

    def run(self):
        gdown.download(self.download_link, self.video_path, None)  #, self.bar)
        self.main.set_video()
# ******************************************** 쓰레드 작업 ******************************************** #
