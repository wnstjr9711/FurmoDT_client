from PySide2.QtWidgets import QLineEdit, QLabel, QListWidgetItem, QTableWidgetItem, QHeaderView, QMessageBox, QComboBox
from PySide2.QtMultimedia import QMediaPlayer, QMediaContent
from PySide2.QtCore import QUrl, QTimer, QThread, QSize, Qt
from PySide2.QtMultimediaWidgets import QVideoWidget
from PySide2.QtGui import QFont
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
        self.table_project.setFont(QFont("나눔명조", 30))

        # 색상 설정
        self.table_project.setStyleSheet("border-radius: 10px;"
                                         "background-color: rgb(255, 255, 255);")
        self.table_work.setStyleSheet('QTableWidget QTableCornerButton::section'
                                      '{border-image: url(files/furmodt-favicon.ico);}')

        # 타이머
        self.timer = QTimer()
        self.timer.setInterval(1)  # 1/1000 sec
        self.timer.timeout.connect(self.timeout)

        # 동영상 플레이어
        self.video_duration = 0
        self.video_player = QMediaPlayer()
        self.video_widget = QVideoWidget(self.videowidget)
        self.video_widget.resize(QSize(480, 360))
        self.video_player.setVideoOutput(self.video_widget)

        self.video_progressbar = roundProgressBar(self.videowidget)
        self.video_progressbar.setGeometry((self.videowidget.width() / 2) - 50,
                                           (self.videowidget.height() / 2) - 50,
                                           100, 100)
        self.video_progressbar.rpb_setBarStyle('Line')
        self.video_progressbar.rpb_setValue(0)
        self.video_progressbar.setVisible(False)

        # 자막
        self.subtitle = QLabel(self.videowidget)
        self.subtitle.setFont(QFont('나눔명조', 7))
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
        self.view_default()

        # 클라이언트 초기화
        self.client = {
            "id": "",
            "qualified": "",
            "GET": None,     # None: project,  project id: work
            "POST": dict(),
        }

        # ******************************************** 동영상 플레이어 조작 이벤트 ******************************************** #
        self.button_play.clicked.connect(self.event_video_button_play)
        self.button_prev.clicked.connect(self.video_pass_prev)
        self.button_next.clicked.connect(self.video_pass_next)
        self.button_stop.clicked.connect(self.video_stop)
        self.soundSlider.valueChanged.connect(self.event_video_sound)
        self.videoSlider.sliderPressed.connect(self.video_pause)
        self.videoSlider.sliderReleased.connect(self.event_video_position)
        self.video_player.durationChanged.connect(self.event_video_duration)
        # ******************************************** 동영상 플레이어 조작 이벤트 ******************************************** #

        # ******************************************** 프로젝트 조작 이벤트 ******************************************** #
        # 생성
        self.button_create_project.clicked.connect(self.event_project_input_visible)
        self.buttonbox_create.accepted.connect(self.event_project_create_accept)
        self.buttonbox_create.rejected.connect(self.event_project_input_visible)
        # 입장
        self.table_project.itemDoubleClicked.connect(self.event_project_join)
        # ******************************************** 프로젝트 조작 이벤트 ******************************************** #

        # ******************************************** 작업 조작 이벤트 ******************************************** #
        self.button_work_quit.clicked.connect(self.view_project)
        self.button_add_language.clicked.connect(self.event_work_add_language)
        self.button_delete_language.clicked.connect(self.event_work_delete_language)
        self.button_work_save.clicked.connect(self.event_work_export)
        self.button_tc_set.clicked.connect(self.event_work_tc_set)
        self.button_tc_in.clicked.connect(self.event_work_tc_in)
        self.button_tc_out.clicked.connect(self.event_work_tc_out)
        self.table_work.itemChanged.connect(self.event_work_update)
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
        self.client['POST'].clear()

    # 타이머 함수
    def timeout(self):
        self.set_playtime(self.video_player.position())
        self.videoSlider.setValue(self.video_player.position())
        if self.videoSlider.value() == self.video_duration:
            self.video_stop()
        if self.subtitle_index < len(self.subtitle_paired):
            in_out = list(map(lambda x: self.time_to_milli(x), (self.table_work.item(self.subtitle_paired[self.subtitle_index], i).text() for i in (0, 1))))
            if self.subtitle_tc != in_out:
                self.subtitle_tc = in_out
            index = self.subtitle_paired[self.subtitle_index]
            if self.video_player.position() >= self.subtitle_tc[1]:
                if self.subtitle.text() != '':
                    self.subtitle.setText('')
                    self.table_work.verticalHeaderItem(index).setBackgroundColor("white")
                self.subtitle_index += 1
            elif self.video_player.position() >= self.subtitle_tc[0]:
                text = self.table_work.item(self.subtitle_paired[self.subtitle_index], 2).text()
                if self.subtitle.text() != text:
                    self.subtitle.setText(text.replace('|', '\n'))  # 2 = 테스트용 첫번째 언어
                    self.table_work.setVerticalHeaderItem(index, QTableWidgetItem(str(index + 1)))
                    self.table_work.verticalHeaderItem(index).setBackgroundColor("yellow")

    # ******************************************** 화면 전환 함수 ******************************************** #
    def view_default(self):
        for i in range(2):
            self.table_work.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)
        # 작업 화면 초기화 #
        self.project_input.setVisible(False)
        self.work_widget.setVisible(False)
        self.main.resize(QSize(1080, 720))

    def view_project(self):
        self.client['GET'] = None
        self.table_work.clear()
        self.table_work.setRowCount(200)
        self.subtitle.clear()
        self.subtitle_paired.clear()
        self.subtitle_index = 0
        self.subtitle_tc = [sys.maxsize, sys.maxsize]
        self.work_widget.setVisible(False)
        self.project_widget.setVisible(True)
        self.project_input.setVisible(False)
        self.project_list.clear()
        self.table_project.clear()
        self.video_player.setMedia(QMediaContent())
        # self.duration = 0
        # self.videoSlider.setMaximum(self.duration)
        # self.stop_video()
        self.video_progressbar.rpb_setValue(0)
        self.video_progressbar.setVisible(False)

    def view_work(self):
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
                self.table_project.addItem(item)
        # 자막 화면 갱신
        else:
            if 'update' not in ret:  # 최초 전체 갱신
                new_work_data = read_json(ret['work'])
                # 프로젝트 확인
                self.work_video = ret['metadata']
                self.event_video_set()
                # header 갱신
                self.work_header = new_work_data.columns.tolist()
                self.table_work.setColumnCount(len(self.work_header))
                self.table_work.setHorizontalHeaderLabels(self.work_header)
                # 작업 갱신
                for row in range(len(new_work_data.index)):
                    for column in range(len(new_work_data.columns)):
                        target = new_work_data.iloc[row, column]
                        if target:
                            item = QTableWidgetItem(str(target))
                            self.work_who = (row, column, item.text())
                            self.table_work.setItem(row, column, item)
            else:  # 부분 갱신
                if self.work_header != ret['header']:
                    delete_language = set(self.work_header).difference(set(ret['header']))
                    if delete_language:
                        self.table_work.removeColumn(self.work_header.index(delete_language.pop()))
                    self.work_header = ret['header']
                    self.table_work.setColumnCount(len(self.work_header))
                    self.table_work.setHorizontalHeaderLabels(self.work_header)
                for update in ret['update']:
                    row, column, text = update
                    if not self.table_work.item(row, column) or self.table_work.item(row, column).text() != text:
                        self.work_who = update
                        self.table_work.setItem(row, column, QTableWidgetItem(text))
            if self.video_progressbar.isVisible():
                if self.video_player.isVideoAvailable():
                    self.video_progressbar.setVisible(False)
    # ******************************************** 화면 전환 함수 ******************************************** #

    # ******************************************** 동영상 플레이 이벤트 함수 ******************************************** #
    def video_play(self):
        self.button_play.setText('❚❚')
        self.video_player.play()
        self.timer.start()
        self.button_play.setShortcut(u"Space")

    def video_pause(self):
        self.button_play.setText('▶')
        self.timer.stop()
        self.video_player.pause()
        self.button_play.setShortcut(u"Space")

    def video_stop(self):
        self.video_pause()
        self.videoSlider.setValue(0)
        self.event_video_position()

    def video_pass_prev(self):
        if self.video_player.isVideoAvailable():
            target = self.video_player.position() - 5000
            self.videoSlider.setValue(target)
            if self.videoSlider.value() == 0:
                self.video_stop()
            else:
                self.event_video_position()
                self.video_play()

    def video_pass_next(self):
        if self.video_player.isVideoAvailable():
            target = self.video_player.position() + 5000
            self.videoSlider.setValue(target)
            if self.videoSlider.value() == self.video_duration:
                self.video_stop()
            else:
                self.event_video_position()
                self.video_play()

    def event_video_button_play(self):
        if self.button_play.text() == '❚❚':
            self.video_pause()
        else:
            if self.video_player.isVideoAvailable():
                self.video_play()

    def set_playtime(self, start):
        start = str(datetime.timedelta(milliseconds=start)).split(':')
        end = str(datetime.timedelta(milliseconds=self.video_duration)).split(':')
        start_sec, end_sec = start.pop(-1)[:6], end.pop(-1)[:6]
        self.playtime.setText('{}:{}:{} / {}:{}:{}'.format(*start, start_sec, *end, end_sec))

    def event_video_sound(self):
        self.video_player.setVolume(self.soundSlider.value())
        self.sound.setText(str(self.soundSlider.value()))

    def event_video_duration(self):
        self.video_duration = self.video_player.duration()
        self.videoSlider.setMaximum(self.video_duration)
        self.video_stop()

    def event_video_position(self):
        self.video_player.setPosition(self.videoSlider.value())
        self.set_playtime(self.videoSlider.value())
        # 자막 위치 찾기
        self.subtitle.setText('')
        time_codes = [self.table_work.item(i, 0).text() for i in self.subtitle_paired]
        try:
            self.table_work.verticalHeaderItem(self.subtitle_paired[self.subtitle_index]).setBackgroundColor("white")
        except (IndexError, AttributeError):
            pass
        self.subtitle_index = bisect.bisect_left(time_codes, self.milli_to_time(self.videoSlider.value()))

    def event_video_set(self):
        filename = self.work_video['video']
        location = os.path.join(os.getcwd(), FOLDER)
        video_path = os.path.join(location, filename)
        self.video_progressbar.setVisible(True)
        if not os.path.exists(video_path):
            self.video_load(location, video_path, self.work_video['url'].split('/')[-2])
        else:
            if self.video_progressbar.rpb_textValue != '100%':
                self.video_progressbar.rpb_setValue(100)
            media = QMediaContent(QUrl.fromLocalFile(os.path.join(os.getcwd(), FOLDER, filename)))
            self.video_player.setMedia(media)

    def video_load(self, location, video_path, fileid):
        if not os.path.exists(location):
            os.mkdir(location)
        self.thread_video_download = DownLoadThread(self, 'https://drive.google.com/uc?id=' + fileid, video_path)
        self.thread_video_download.start()
    # ******************************************** 동영상 플레이 이벤트 함수 ******************************************** #

    # ******************************************** 프로젝트 이벤트 함수 ******************************************** #
    def event_project_input_visible(self):
        self.project_input.setVisible(not self.project_input.isVisible())

    def event_project_create_accept(self):
        self.project_input.setVisible(False)
        project = list(filter(lambda x: type(x) == QLineEdit, self.project_input.children()))
        project_name, file_url = map(lambda x: x.text(), project)
        filename = gdown.getfilename(file_url)
        if filename is not None:
            self.client['POST'][1] = [project_name, file_url, filename]
            clear = list(map(lambda x: x.clear(), project))
        else:
            err = QMessageBox()
            err.information(self.main, 'error', 'invalid url!')

    def event_project_join(self):
        self.client['GET'] = self.table_project.currentItem().text()
        self.view_work()
    # ******************************************** 프로젝트 이벤트 함수 ******************************************** #

    # ******************************************** 작업 이벤트 함수 ******************************************** #
    def event_work_add_language(self):
        select_language = QMessageBox()
        select_language.setWindowTitle('언어선택')
        select_language.setStandardButtons(select_language.Yes | select_language.No)
        select_language.setGeometry(self.main.x() + self.main.width()/2, self.main.y() + self.main.height()/2,
                                    select_language.width(), select_language.height())
        combobox = QComboBox(select_language)
        combobox.setGeometry(45, combobox.y(), combobox.width(), combobox.height())
        for lang in ['한국어', '영어', '베트남어', '일본어', '중국어']:
            combobox.addItem(lang)
        if select_language.exec_() == select_language.Yes:
            msg, num = combobox.currentText(), 1
            if msg in self.work_header:
                while '{} ({})'.format(msg, num) in self.work_header:
                    num += 1
                msg = '{} ({})'.format(msg, num)
            self.client['POST'][3] = [msg]

    def event_work_update(self):
        if self.work_who:
            row_position = self.work_who[0]
            self.work_who = None
        else:
            cell = self.table_work.currentItem()
            cell_data = (cell.row(), cell.column(), cell.text())
            # TC Validation: format
            if cell_data[1] in (0, 1):
                try:
                    assert cell_data[2] == '' or bool(re.match(r"\d{2}:\d{2}:\d{2}.\d{3}$", cell_data[2]))
                    self.client['POST'][5] = [cell_data]
                    row_position = cell.row()
                except AssertionError:
                    self.table_work.setItem(cell_data[0], cell_data[1], QTableWidgetItem(0))
                    row_position = 0
            else:
                self.client['POST'][5] = [cell_data]
                row_position = cell.row()
        if row_position + 50 >= self.table_work.rowCount():  # QTableWidget 행 추가
            self.table_work.setRowCount(self.table_work.rowCount() + 100)
        # TC Validation: set
        index = bisect.bisect_left(self.subtitle_paired, row_position)
        if False not in map(lambda x: bool(x.text()) if x else False, (self.table_work.item(row_position, i) for i in (0, 1))):
            if index == len(self.subtitle_paired) or self.subtitle_paired[index] != row_position:
                self.subtitle_paired.insert(index, row_position)
                if index < self.subtitle_index:
                    self.subtitle_index += 1
        else:
            if index < len(self.subtitle_paired) and self.subtitle_paired[index] == row_position:
                check = self.subtitle_paired.pop(index)
                if index == self.subtitle_index and self.table_work.verticalHeaderItem(check):
                    self.table_work.verticalHeaderItem(check).setBackgroundColor("white")
                elif index < self.subtitle_index:
                    self.subtitle_index -= 1
        # TODO TimeCode validation check: IN OUT complex

    def event_work_add_subtitle(self, url):
        subs = pysrt.open(url)
        srt = list()
        for i in subs:
            srt.append((i.index - 1, 0, str(i.start).replace(',', '.')))
            srt.append((i.index - 1, 1, str(i.end).replace(',', '.')))
            srt.append((i.index - 1, 2, str(i.text).replace('\n', '|')))
        self.client['POST'][5] = srt

    def event_work_export(self):
        sub = pysrt.SubRipFile()
        empty_text = list()
        for index in self.subtitle_paired:
            item = self.table_work.item(index, 0), self.table_work.item(index, 1), self.table_work.item(index, 2)
            if item[2]:
                item = pysrt.SubRipItem(index + 1, item[0].text().replace('.', ','), item[1].text().replace('.', ','),
                                        item[2].text().replace('|', '\n'))
                sub.append(item)
            else:
                empty_text.append(index)
        if empty_text:
            err = QMessageBox()
            err.information(self.main, 'error', 'no text in {}'.format(empty_text))
        sub.save(os.path.join(FOLDER, '{}.srt'.format(self.work_video['video'])))

    def event_work_delete_language(self):
        select_language = QMessageBox()
        select_language.setWindowTitle('언어선택')
        select_language.setStandardButtons(select_language.Yes | select_language.No)
        select_language.setGeometry(self.main.x() + self.main.width()/2, self.main.y() + self.main.height()/2,
                                    select_language.width(), select_language.height())
        combobox = QComboBox(select_language)
        combobox.setGeometry(45, combobox.y(), combobox.width(), combobox.height())
        for lang in self.work_header[3:]:
            combobox.addItem(lang)
        if select_language.exec_() == select_language.Yes:
            if combobox.currentText():
                self.client['POST'][4] = [combobox.currentText()]

    def event_work_tc_set(self):
        tc = self.video_player.position()
        row = self.table_work.currentIndex().row()
        self.tc_put(0, tc, row)
        if row > 0 and (self.table_work.item(row - 1, 1) is None or not self.table_work.item(row - 1, 1).text()):
            self.tc_put(1, tc, row - 1)
        self.table_work.setCurrentCell(row + 1, 0)

    def event_work_tc_in(self):
        row = self.table_work.currentIndex().row()
        self.tc_put(0, self.video_player.position(), row)

    def event_work_tc_out(self):
        row = self.table_work.currentIndex().row()
        self.tc_put(1, self.video_player.position(), row)
        self.table_work.setCurrentCell(row + 1, 0)

    def tc_put(self, column, tc, row):
        row = row if row >= 0 else 0
        self.table_work.setCurrentCell(row, column)
        item = QTableWidgetItem(self.milli_to_time(tc))
        self.table_work.setItem(row, column, item)
    # ******************************************** 작업 이벤트 함수 ******************************************** #


# ******************************************** 쓰레드 작업 ******************************************** #
class DownLoadThread(QThread):
    def __init__(self, main, download_link, video_path):
        super(DownLoadThread, self).__init__()
        self.main = main
        self.download_link = download_link
        self.video_path = video_path

    def run(self):
        gdown.download(self.download_link, self.video_path, self.main.video_progressbar)
        self.main.event_video_set()
# ******************************************** 쓰레드 작업 ******************************************** #
