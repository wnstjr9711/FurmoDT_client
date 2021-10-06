from PySide2.QtCore import QUrl, QTimer, QThread, QSize, Qt
from PySide2.QtGui import QFont, QIcon
from PySide2.QtMultimediaWidgets import QVideoWidget
from PySide2.QtMultimedia import QMediaPlayer, QMediaPlaylist
from PySide2.QtWidgets import QLineEdit, QLabel, QListWidgetItem, QTableWidgetItem, QHeaderView, QMessageBox
from PySide2extn.RoundProgressBar import roundProgressBar
from ui_main import Ui_MainWindow
from pandas import read_json
import datetime
import bisect
import pysrt
import gdown
import sys
import os
import re

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
        self.main.setWindowIcon(QIcon('files/furmodt-favicon.ico'))

        # 색상 설정
        self.project_table.setStyleSheet("border-radius: 10px;"
                                         "background-color: rgb(255, 255, 255);")
        self.work_table.setStyleSheet('QTableWidget QTableCornerButton::section'
                                      '{border-image: url(files/furmodt-favicon.ico);}')

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

        self.progressbar = roundProgressBar(self.videowidget)
        self.progressbar.setGeometry((self.videowidget.width() / 2) - 50,
                                     (self.videowidget.height() / 2) - 50,
                                     100, 100)
        self.progressbar.rpb_setBarStyle('Line')
        self.progressbar.rpb_setValue(0)
        self.progressbar.setVisible(False)

        # 자막
        self.subtitle = QLabel(self.videowidget)
        x, y = self.video_widget.width(), int(self.video_widget.height()/8)
        self.subtitle.setGeometry(0, self.videowidget.height() - y, x, y)
        self.subtitle.setStyleSheet("background-color: black;"
                                    "color: white;")
        self.subtitle.setAlignment(Qt.AlignCenter)

        self.subtitle_paired = list()
        self.subtitle_index = 0
        self.subtitle_tc = [sys.maxsize, sys.maxsize]

        # 프로젝트 목록
        self.project_list = list()

        # 작업 영상 url, name
        self.work_video = dict()
        self.work_header = list()
        self.thread_video_download = None
        self.work_who = None  # update 주체가 다를 때 변동사항 재전송 방지

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
        self.quit_work.clicked.connect(self.project_view)
        self.add_work.clicked.connect(self.add_language)
        self.work_table.itemChanged.connect(self.update_work)
        # ******************************************** 작업 조작 이벤트 ******************************************** #

    @staticmethod
    def milli_to_time(milli):
        ms = milli % 1000
        s = milli // 1000
        h = s // 3600
        s %= 3600
        m = s // 60
        s %= 60
        return '{:02}:{:02}:{:02}.{:03}'.format(h, m, s, ms)

    @staticmethod
    def time_to_milli(time):
        h, m, s = time.split(':')
        return int(h) * 60 * 60 * 1000 + int(m) * 60 * 1000 + int(float(s) * 1000)

    # post 메시지 초기화
    def setdefault_client(self):
        self.client['POST'] = {}

    # 타이머 함수
    def timeout(self):
        self.set_playtime(self.player.position())
        self.videoSlider.setValue(self.player.position())
        if self.subtitle_index < len(self.subtitle_paired):
            in_out = list(map(lambda x: self.time_to_milli(x), (self.work_table.item(self.subtitle_paired[self.subtitle_index], i).text() for i in (0, 1))))
            if self.subtitle_tc != in_out:
                self.subtitle_tc = in_out
        if self.player.position() >= self.subtitle_tc[1]:
            if self.subtitle.text() != '':
                self.subtitle.setText('')
                # for i in range(self.work_table.columnCount()):
                #     self.work_table.item(self.subtitle_index, i).setBackgroundColor("white")
            self.subtitle_index += 1
        elif self.player.position() >= self.subtitle_tc[0]:
            text = self.work_table.item(self.subtitle_paired[self.subtitle_index], 2).text()
            if self.subtitle.text() != text:
                self.subtitle.setText(text.replace('|', '\n'))  # 2 = 테스트용 첫번째 언어
                # for i in range(self.work_table.columnCount()):
                #     self.work_table.item(self.subtitle_index, i).setBackgroundColor("yellow")

    # ******************************************** 화면 전환 함수 ******************************************** #
    def default_view(self):
        for i in range(2):
            self.work_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)
        # 작업 화면 초기화 #
        self.project_input.setVisible(False)
        self.work_widget.setVisible(False)
        self.main.resize(QSize(1080, 720))

    def project_view(self):
        self.client['GET'] = None
        self.timer.stop()
        self.work_table.clear()
        self.work_table.setRowCount(200)
        self.subtitle.clear()
        self.subtitle_paired.clear()
        self.subtitle_index = 0
        self.subtitle_tc = [sys.maxsize, sys.maxsize]
        self.work_widget.setVisible(False)
        self.project_widget.setVisible(True)
        self.project_input.setVisible(False)
        self.project_list.clear()
        self.project_table.clear()
        self.playlist.clear()
        self.player.setPlaylist(self.playlist)
        self.progressbar.rpb_setValue(0)

    def work_view(self):
        self.project_widget.setVisible(False)
        self.work_widget.setVisible(True)

    def refresh(self, ret):
        # 프로젝트 목록 갱신
        if type(ret) == list:
            self.work_video = None
            add = set(ret).difference(self.project_list)
            for row in sorted(add):
                self.project_list.append(row)
                item = QListWidgetItem(row)
                item.setTextAlignment(Qt.AlignHCenter)
                self.project_table.addItem(item)
        # 자막 화면 갱신
        else:
            if 'update' not in ret:  # 최초 전체 갱신
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
                for row in range(len(new_work_data.index)):
                    for column in range(len(new_work_data.columns)):
                        target = new_work_data.iloc[row, column]
                        if target:
                            item = QTableWidgetItem(str(target))
                            self.work_who = (row, column, item.text())
                            self.work_table.setItem(row, column, item)
            else:  # 부분 갱신
                if self.work_header != ret['header']:
                    self.work_header = ret['header']
                    self.work_table.setColumnCount(len(self.work_header))
                    self.work_table.setHorizontalHeaderLabels(self.work_header)
                for update in ret['update']:
                    row, column, text = update
                    if not self.work_table.item(row, column) or self.work_table.item(row, column).text() != text:
                        self.work_who = update
                        self.work_table.setItem(row, column, QTableWidgetItem(text))
            if self.progressbar.isVisible():
                if self.player.isVideoAvailable():
                    self.progressbar.setVisible(False)
    # ******************************************** 화면 전환 함수 ******************************************** #

    # ******************************************** 동영상 플레이 이벤트 함수 ******************************************** #
    def play_video(self):
        self.play.setText('❚❚')
        self.player.play()
        self.timer.start()
        self.play.setShortcut(u"Space")

    def pause_video(self):
        self.play.setText('▶')
        self.timer.stop()
        self.player.pause()
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
        self.pause_video()
        self.videoSlider.setValue(0)
        self.set_position()

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
        if not self.player.isVideoAvailable():
            self.stop_video()
            self.player.setMedia(self.player.media())
        else:
            self.stop_video()

    def set_position(self):
        self.player.setPosition(self.videoSlider.value())
        self.set_playtime(self.videoSlider.value())
        # 자막 위치 찾기
        self.subtitle.setText('')
        time_codes = [self.work_table.item(i, 0).text() for i in self.subtitle_paired]
        self.subtitle_index = bisect.bisect_left(time_codes, self.milli_to_time(self.videoSlider.value()))

    def set_video(self):
        filename = self.work_video['video']
        location = os.path.join(os.getcwd(), FOLDER)
        video_path = os.path.join(location, filename)
        self.progressbar.setVisible(True)
        if not os.path.exists(video_path):
            self.load_video_event(location, video_path, self.work_video['url'].split('/')[-2])
        else:
            if self.progressbar.rpb_textValue != '100%':
                self.progressbar.rpb_setValue(100)
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
        filename = gdown.getfilename(file_url)
        if filename is not None:
            self.client['POST'][1] = [project_name, file_url, filename]
            clear = list(map(lambda x: x.clear(), project))
        else:
            err = QMessageBox()
            err.setText("invalid url!")
            err.setWindowTitle('error')
            err.exec_()

    def create_reject(self):
        self.project_input.setVisible(False)

    def join_project(self):
        self.client['GET'] = self.project_table.currentItem().text()
        self.work_view()
    # ******************************************** 프로젝트 이벤트 함수 ******************************************** #

    # ******************************************** 작업 이벤트 함수 ******************************************** #
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
        if self.work_who:
            row_position = self.work_who[0]
            self.work_who = None
        else:
            cell = self.work_table.currentItem()
            cell_data = (cell.row(), cell.column(), cell.text())
            # TC Validation: format
            if cell_data[1] in (0, 1):
                try:
                    assert cell_data[2] == '' or bool(re.match(r"\d{2}:\d{2}:\d{2}.\d{3}$", cell_data[2]))
                    self.client['POST'][4] = [cell_data]
                    row_position = cell.row()
                except AssertionError:
                    self.work_table.setItem(cell_data[0], cell_data[1], QTableWidgetItem(0))
                    row_position = 0
            else:
                self.client['POST'][4] = [cell_data]
                row_position = cell.row()
        if row_position + 50 >= self.work_table.rowCount():  # QTableWidget 행 추가
            self.work_table.setRowCount(self.work_table.rowCount() + 100)
        # TC Validation: set
        index = bisect.bisect_left(self.subtitle_paired, row_position)
        if False not in map(lambda x: bool(x.text()) if x else False, (self.work_table.item(row_position, i) for i in (0, 1))):
            if index == len(self.subtitle_paired) or self.subtitle_paired[index] != row_position:
                self.subtitle_paired.insert(index, row_position)
                if index < self.subtitle_index:
                    self.subtitle_index += 1
        else:
            if index < len(self.subtitle_paired) and self.subtitle_paired[index] == row_position:
                self.subtitle_paired.pop(index)
                if index < self.subtitle_index:
                    self.subtitle_index -= 1
        # TODO TimeCode validation check: IN OUT complex

    def add_subtitle(self, url):
        subs = pysrt.open(url)
        srt = list()
        for i in subs:
            srt.append((i.index - 1, 0, str(i.start).replace(',', '.')))
            srt.append((i.index - 1, 1, str(i.end).replace(',', '.')))
            srt.append((i.index - 1, 2, str(i.text).replace('\n', '|')))
        self.client['POST'][4] = srt

    # def delete_language(self):
    #     self.work_table.removeColumn(3)
    #     self.client['POST'][123] = remove language
    # ******************************************** 작업 이벤트 함수 ******************************************** #


# ******************************************** 쓰레드 작업 ******************************************** #
class DownLoadThread(QThread):
    def __init__(self, main, download_link, video_path):
        super(DownLoadThread, self).__init__()
        self.main = main
        self.download_link = download_link
        self.video_path = video_path

    def run(self):
        gdown.download(self.download_link, self.video_path, self.main.progressbar)
        self.main.set_video()
# ******************************************** 쓰레드 작업 ******************************************** #
