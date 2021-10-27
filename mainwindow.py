from PySide2.QtWidgets import QLineEdit, QLabel, QListWidgetItem, QTableWidgetItem, QHeaderView, QMessageBox, QComboBox, QMainWindow
from PySide2.QtMultimedia import QMediaPlayer, QMediaContent
from PySide2.QtCore import QUrl, QTimer, QSize, Qt
from PySide2.QtMultimediaWidgets import QVideoWidget
from PySide2.QtGui import QFont
from PySide2extn.RoundProgressBar import roundProgressBar
from ui_main import Ui_MainWindow
from pandas import read_json
import datetime
import config
import bisect
import pysrt
import gdown
import sys
import re
import os

COLOR = ['red', 'cyan', 'magenta', 'gray', 'blue']


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, client, authority_level):
        super(MainWindow, self).__init__()

        # ui 설정
        self.setupUi(self)

        # 클라이언트 초기화
        self.client = {
            "id": client,
            "authority_level": authority_level,
            "GET": None,     # None: project,  project id: work
            "POST": dict(),
        }

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
        self.video_player.setVideoOutput(self.video_widget)

        self.video_progressbar = roundProgressBar(self.videowidget)
        self.video_progressbar.rpb_setBarStyle('Line')
        self.video_progressbar.rpb_setValue(0)
        self.video_progressbar.setVisible(False)

        # 자막
        self.subtitle = QLabel(self.videowidget)
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
        self.worker = dict()

        # 초기화면 설정
        self.view_default()
        self.setAcceptDrops(True)

        # ******************************************** 동영상 플레이어 조작 이벤트 ******************************************** #
        self.button_play.clicked.connect(self.event_video_button_play)
        self.button_prev.clicked.connect(self.video_pass_prev)
        self.button_next.clicked.connect(self.video_pass_next)
        self.button_stop.clicked.connect(self.video_stop)
        self.soundSlider.valueChanged.connect(self.event_video_sound)
        self.videoSlider.sliderPressed.connect(self.video_pause)
        self.videoSlider.sliderReleased.connect(self.event_video_position)
        self.video_player.durationChanged.connect(self.event_video_duration)
        self.video_player.currentMediaChanged.connect(self.event_video_clear_macos)
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
        self.table_work.currentCellChanged.connect(self.event_work_video_move)
        # ******************************************** 작업 조작 이벤트 ******************************************** #

    # ******************************************** 이벤트 오버라이딩 ******************************************** #
    def dragEnterEvent(self, e):
        if self.work_widget.isVisible():
            e.accept()

    def dragMoveEvent(self, e):
        target = self.work_widget
        x_range = range(*(target.x(), target.x() + target.width() + 1))
        y_range = range(*(target.y(), target.y() + target.height() + 1))
        if e.pos().x() in x_range and e.pos().y() in y_range:
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.event_work_add_subtitle(e.mimeData().urls()[0].toLocalFile())

    def resizeEvent(self, e):
        self.table_project.setFont(QFont('Nanum Myeongjo', int(self.project_widget.height()/20*0.8)))
        self.video_widget.resize(self.videowidget.size())
        self.video_progressbar.setGeometry((self.videowidget.width() / 2) - 50,
                                           (self.videowidget.height() / 2) - 50,
                                           100, 100)
        x, y = self.video_widget.width(), int(self.video_widget.height() / 8)
        self.subtitle.setGeometry(0, self.videowidget.height() - y, x, y)
        self.subtitle.setFont(QFont('Nanum Myeongjo', int(self.subtitle.height() * 0.7 / 3)))
    # ******************************************** 이벤트 오버라이딩 ******************************************** #

    # ******************************************** 타이머 ******************************************** #
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

    def timeout(self):
        self.set_playtime(self.video_player.position())
        self.videoSlider.setValue(self.video_player.position())
        if self.videoSlider.value() == self.video_duration:
            self.video_stop()
        if self.subtitle_index < len(self.subtitle_paired):
            in_out = list(map(lambda x: self.time_to_milli(x),
                              (self.table_work.item(self.subtitle_paired[self.subtitle_index], i).text()
                               for i in (0, 1))))
            if self.subtitle_tc != in_out:
                self.subtitle_tc = in_out
            index = self.subtitle_paired[self.subtitle_index]
            if self.video_player.position() >= self.subtitle_tc[1]:
                if self.subtitle.text() != '':
                    self.subtitle.setText('')
                    self.table_work.verticalHeaderItem(index).setBackgroundColor("white")
                self.subtitle_index += 1
            elif self.video_player.position() >= self.subtitle_tc[0]:
                subtitle = self.table_work.item(self.subtitle_paired[self.subtitle_index], 2)  # 2 = 테스트용 첫번째 언어
                if subtitle and self.subtitle.text() != subtitle.text():
                    self.subtitle.setText(subtitle.text().replace('|', '\n'))
                    self.table_work.setVerticalHeaderItem(index, QTableWidgetItem(str(index + 1)))
                    self.table_work.verticalHeaderItem(index).setBackgroundColor("yellow")
            elif self.video_player.position() < self.subtitle_tc[0]:
                if self.subtitle_index > 0:
                    self.subtitle_index -= 1
    # ******************************************** 타이머 ******************************************** #

    # ******************************************** 화면 상태 함수 ******************************************** #
    # post 메시지 초기화
    def setdefault_client(self):
        for key in tuple(i for i in self.client['POST'].keys()):
            self.client['POST'].pop(key)

    def view_default(self):
        for i in range(2):
            self.table_work.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)
        # 작업 화면 초기화 #
        self.project_input.setVisible(False)
        self.work_widget.setVisible(False)
        self.resize(QSize(1080, 720))

    def view_project(self):
        self.client['GET'] = None
        del self.worker
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
        self.video_progressbar.rpb_setValue(0)
        self.video_progressbar.setVisible(False)

    def view_work(self):
        self.project_widget.setVisible(False)
        self.work_widget.setVisible(True)
        self.table_work.setCurrentCell(0, 1)

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

                try:
                    change = list()
                    for worker in list(self.worker.keys()):
                        value = ret['worker'].get(worker)
                        if value:
                            ret['worker'].pop(worker)
                            if value != self.worker[worker]:
                                self.table_work.item(*self.worker[worker]).setBackgroundColor('white')
                                self.worker[worker] = value
                                change.append(worker)
                        else:
                            self.table_work.item(*self.worker[worker]).setBackgroundColor('white')
                            self.worker.pop(worker)
                    for worker in ret['worker']:
                        self.worker[worker] = ret['worker'][worker]
                        change.append(worker)
                    if change:
                        for key in change:
                            if key == self.client['id']:
                                continue
                            idx = list(self.worker).index(key)
                            color = COLOR[idx]
                            r, c = self.worker[key]
                            if not self.table_work.item(r, c):
                                self.table_work.setItem(r, c, QTableWidgetItem(''))
                            self.table_work.item(r, c).setBackgroundColor(color)

                except AttributeError:
                    self.worker = dict()
                self.workers.setText('참여자: ' + ', '.join(list(self.worker)))

            if self.video_progressbar.isVisible():
                if self.video_player.isVideoAvailable():
                    self.video_progressbar.setVisible(False)
    # ******************************************** 화면 상태 함수 ******************************************** #

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

    def event_video_clear_macos(self):
        if not self.video_player.media().canonicalUrl().url():
            self.video_duration = 0
            self.videoSlider.setMaximum(self.video_duration)
            self.video_stop()

    def event_video_set(self):
        filename = self.work_video['video']
        location = os.path.join(os.getcwd(), config.FOLDER)
        video_path = os.path.join(location, filename)
        self.video_progressbar.setVisible(True)
        if not os.path.exists(video_path):
            self.video_load(location, video_path, self.work_video['url'].split('/')[-2])
        else:
            if self.video_progressbar.rpb_textValue != '100%':
                self.video_progressbar.rpb_setValue(100)
            media = QMediaContent(QUrl.fromLocalFile(os.path.join(os.getcwd(), config.FOLDER, filename)))
            self.video_player.setMedia(media)

    def video_load(self, location, video_path, fileid):
        if not os.path.exists(location):
            os.mkdir(location)
        self.thread_video_download = gdown.DownLoadThread(self, 'https://drive.google.com/uc?id=' + fileid, video_path)
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
            err.information(self, 'error', 'invalid url!')

    def event_project_join(self):
        self.client['GET'] = self.table_project.currentItem().text()
        self.view_work()
    # ******************************************** 프로젝트 이벤트 함수 ******************************************** #

    # ******************************************** 작업 이벤트 함수 ******************************************** #
    def event_work_add_language(self):
        select_language = CustomQMessageBox(self)
        for lang in ['한국어', '영어', '베트남어', '일본어', '중국어']:
            select_language.combobox.addItem(lang)
        if select_language.exec_() == select_language.Yes:
            msg, num = select_language.combobox.currentText(), 1
            if msg in self.work_header:
                while '{} ({})'.format(msg, num) in self.work_header:
                    num += 1
                msg = '{} ({})'.format(msg, num)
            self.client['POST'][3] = [msg]

    def event_work_delete_language(self):
        select_language = CustomQMessageBox(self)
        for lang in self.work_header[3:]:
            select_language.combobox.addItem(lang)
        if select_language.exec_() == select_language.Yes:
            if select_language.combobox.currentText():
                self.client['POST'][4] = [select_language.combobox.currentText()]

    def event_work_update(self):
        if self.work_who:
            row_position = self.work_who[0]
            self.work_who = None
        else:
            try:
                cell = self.table_work.currentItem()
                cell_data = (cell.row(), cell.column(), cell.text())
            except AttributeError:
                return
            # TC Validation: format
            if cell_data[1] in (0, 1):
                try:
                    assert cell_data[2] == '' or bool(re.match(r"\d{2}:\d{2}:\d{2}.\d{3}$", cell_data[2]))
                    if 5 in self.client['POST']:
                        self.client['POST'][5].append(cell_data)
                    else:
                        self.client['POST'][5] = [cell_data]
                    row_position = cell.row()
                except AssertionError:
                    self.table_work.setItem(cell_data[0], cell_data[1], QTableWidgetItem(''))
                    row_position = 0
            else:
                self.client['POST'][5] = [cell_data]
                row_position = cell.row()
        if row_position + 50 >= self.table_work.rowCount():  # QTableWidget 행 추가
            self.table_work.setRowCount(self.table_work.rowCount() + 100)
        # TC Validation: set
        index = bisect.bisect_left(self.subtitle_paired, row_position)
        if False not in map(lambda x: bool(x.text()) if x else False,
                            (self.table_work.item(row_position, i) for i in (0, 1))):
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
        num = 1
        for index in self.subtitle_paired:
            item = self.table_work.item(index, 0), self.table_work.item(index, 1), self.table_work.item(index, 2)
            if item[2]:
                item = pysrt.SubRipItem(num, item[0].text().replace('.', ','),
                                        item[1].text().replace('.', ','),
                                        item[2].text().replace('|', '\n'))
                sub.append(item)
                num += 1
            else:
                empty_text.append(index)
        if empty_text:
            err = QMessageBox()
            err.information(self, 'error', 'no text in {}'.format(empty_text))
        sub.save(os.path.join(config.FOLDER, '{}.srt'.format(self.work_video['video'])))

    def event_work_tc_set(self):
        tc = self.video_player.position()
        row = self.table_work.currentIndex().row()
        self.tc_put(1, tc, row)
        self.tc_put(0, tc, row + 1)
        self.table_work.setCurrentCell(row + 1, 1)

    def event_work_tc_in(self):
        row = self.table_work.currentIndex().row()
        if self.table_work.item(row, 0):
            self.table_work.setItem(row, 0, None)
        self.tc_put(0, self.video_player.position(), row)
        self.table_work.setCurrentCell(row, 1)

    def event_work_tc_out(self):
        row = self.table_work.currentIndex().row()
        self.tc_put(1, self.video_player.position(), row)
        self.table_work.setCurrentCell(row + 1, 0)

    def tc_put(self, column, tc, row):
        self.table_work.setCurrentCell(row, column)
        item = QTableWidgetItem(self.milli_to_time(tc))
        self.table_work.setItem(row, column, item)

    def event_work_video_move(self):
        self.client['POST'][6] = (self.table_work.currentRow(), self.table_work.currentColumn())
        moveto = self.table_work.item(self.table_work.currentRow(), 0)
        if moveto and moveto.text():
            self.videoSlider.setValue(self.time_to_milli(moveto.text()))
            self.event_video_position()
    # ******************************************** 작업 이벤트 함수 ******************************************** #


class CustomQMessageBox(QMessageBox):
    def __init__(self, parent):
        super(CustomQMessageBox, self).__init__()
        self.setWindowTitle('언어선택')
        self.setStandardButtons(self.Yes | self.No)
        self.setGeometry(int(parent.x() + parent.width() / 2), int(parent.y() + parent.height() / 2),
                         self.width(), self.height())
        self.combobox = QComboBox(self)
        self.combobox.setGeometry(45, self.combobox.y(), self.combobox.width(), self.combobox.height())
