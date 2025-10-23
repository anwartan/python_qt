import cv2
from PyQt6.QtCore import pyqtSignal,QThread
from PyQt6.QtGui import QImage
import numpy
class Camera (QThread):
    signal_frame=pyqtSignal(
        numpy.ndarray
    )
    def __init__(self):
        super().__init__()
        self.cam=cv2.VideoCapture(0)
        self.running=True
        print("mambuat Camera")
    def start(self):
        super().start()
        self.running=True
    def run(self):
        print('menjalankan camera')
        while self.running:
            if not self.cam.isOpened():
                self.cam.open(0)
            ret, frame=self.cam.read()
            self.signal_frame.emit(frame)
        self.cam.release()
    def stop(self):
        self.running=False
        print("camera stopped")