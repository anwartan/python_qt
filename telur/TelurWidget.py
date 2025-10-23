# Subclass QMainWindow to customize your application's main window
from PyQt6.uic import loadUi
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QImage,QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from libcamera import Camera
import cv2
from libdetection import Dectation
from api_client import Apiclient
class TelurWidget(QMainWindow):
    camera=None
    def __init__(self):
        super().__init__()
        loadUi("telur/contoh1.ui",self)
        self.camera=Camera()
        self.detection=Dectation()
        self.masuk.setChecked(True)
        self.spinBox.setEnabled(False)
        self.Stop_button.clicked.connect(self.on_Stop_button)
        self.start_button.clicked.connect(self.on_start_button)
        self.masuk.toggled.connect(self.on_masuk_keluar_change)
        self.keluar.toggled.connect(self.on_masuk_keluar_change)
        self.camera.signal_frame.connect(self.on_frame)
        self.api_client=Apiclient() 
        self.detection.signal_frame_drawed.connect(self.on_drawed_frame)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
    def on_start_button(self):
        print("Start button clicked")
        self.camera.start()
        self.detection.start()
    def on_Stop_button(self):
        print("stop button cliicked")
        self.camera.stop()
        self.detection.stop()
    def on_masuk_keluar_change(self):
        if self.masuk.isChecked():
            self.spinBox.setEnabled(False)
            self.spinBox.setValue(0)
        else:self.spinBox.setEnabled(True)
    def on_frame(self,frame):
        self.detection.setFrame(frame)
    def on_drawed_frame(self,frame,egg_count):
        self.egg_count=egg_count
        objectGambar=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        h, w, x=objectGambar.shape
        qimg=QImage(objectGambar.data,w,h,QImage.Format.Format_RGB888)
        pix=QPixmap.fromImage(qimg).scaled(self.Video_label.size(),Qt.AspectRatioMode.IgnoreAspectRatio)
        self.Video_label.setPixmap(pix)
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Space:
            self.sendData()
    def sendData(self):
        data={
            "jumlah":self.egg_count,
            "price":self.getprice(),
            "jenis":self.gettipe()
        }
        self.api_client.post("http://127.0.0.1:8000/api/telur/store",data)
    def getprice(self):
        return self.spinBox.value()
    def gettipe(self):
        if self.masuk.isChecked():
            return "masuk"
        else:return "keluar"