from PySide2 import QtCore
from PySide2.QtCore import QUrl, QTimer
from PySide2.QtGui import QPalette
from PySide2.QtMultimediaWidgets import QVideoWidget
from PySide2.QtMultimedia import QMediaPlayer, QMediaPlaylist
from PySide2.QtWidgets import QFileDialog, QLineEdit, QTableWidgetItem
from ui_main import Ui_MainWindow
import datetime
import gdown


class AdvancedSetup(Ui_MainWindow):
    def __init__(self, main):
        super().__init__()
        # ui 불러오기
        self.setupUi(main)

        # 초기화면 설정
        self.project_input.setVisible(False)
        self.work_widget.setVisible(False)
        
        self.project_table.setColumnCount(1)
        self.project_table.setHorizontalHeaderLabels(['프로젝트 이름', '동영상 이름'])
        self.project_table.resizeColumnsToContents()
        # self.project_table.setHo
        # self.project_table.
        

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
        pal = QPalette()
        pal.setColor(QPalette.Background, QtCore.Qt.black)
        self.video_widget.setPalette(pal)
        self.player.setVideoOutput(self.video_widget)

        # 클라이언트 초기화
        self.client = {
            "id": "",
            "qualified": "",
            "create_project": list(),
            "get_project_work": None,     # None: project,  project id: work
        }

        # 동영상 플레이어 조작 이벤트
        self.play.clicked.connect(self.play_clicked_event)
        self.prev.clicked.connect(self.pass_prev_video)
        self.next.clicked.connect(self.pass_next_video)
        self.stop.clicked.connect(self.stop_video)
        self.soundSlider.valueChanged.connect(self.sound_slider_event)
        self.videoSlider.sliderPressed.connect(self.video_slider_pressed_event)
        self.videoSlider.sliderReleased.connect(self.video_slider_released_event)
        self.player.durationChanged.connect(self.video_duration_event)
        self.player.positionChanged.connect(self.video_position_event)

        # 프로젝트 조작 이벤트
        self.button_create_project.clicked.connect(self.create_project)
        self.buttonbox_create.accepted.connect(self.create_accept)
        self.buttonbox_create.rejected.connect(self.create_reject)
        
        # 프로젝트
        self.project_table.setItem(0, 0, QTableWidgetItem('as'))

    # 타이머 함수
    def timeout(self):
        self.sec += 1
        self.set_playtime(self.player.position() + self.sec)
        self.videoSlider.setValue(self.player.position())

    # 동영상 플레이 이벤트 함수
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

    def open_video_event(self):
        video = QFileDialog.getOpenFileName(None, "동영상 열기", filter="모든 미디어 파일 (*.mp4 *.avi)")[0]
        # url = 'https://drive.google.com/uc?id=1qNGOzi_PgHNaM056GeZlD6dKeg3JjmWo'
        # gdown.download(url, 'abc', quiet=False)
        # 시간 tqdm
        # try:
        #     total = res.headers.get("Content-Length")
        #     if total is not None:
        #         total = int(total)
        #     if not quiet:
        #         pbar = tqdm.tqdm(total=total, unit="B", unit_scale=True)
        #     t_start = time.time()
        #     for chunk in res.iter_content(chunk_size=CHUNK_SIZE):
        #         f.write(chunk)
        #         if not quiet:
        #             pbar.update(len(chunk))
        #         if speed is not None:
        #             elapsed_time_expected = 1.0 * pbar.n / speed
        #             elapsed_time = time.time() - t_start
        #             if elapsed_time < elapsed_time_expected:
        #                 time.sleep(elapsed_time_expected - elapsed_time)
        #     if not quiet:
        #         pbar.close()
        #     if tmp_file:
        #         f.close()
        #         shutil.move(tmp_file, output)

        if video:
            self.playlist.clear()
            self.playlist.addMedia(QUrl(video))
            self.player.setPlaylist(self.playlist)

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

    # 프로젝트 이벤트 함수
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

    def refresh(self):
        # 프로젝트 목록 갱신
        if not self.client['get_project_work']:

            pass
    # 프로젝트 뷰어
    # def show_table(self):
    #     if self.client
