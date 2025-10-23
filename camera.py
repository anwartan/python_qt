import sys
from PyQt6.uic import loadUi
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QImage,QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from libcamera import Camera
import cv2
from libdetection import Dectation
from api_client import Apiclient
# Subclass QMainWindow to customize your application's main window
from telur.TelurWidget import TelurWidget
app = QApplication(sys.argv)

window = TelurWidget()
window.show()

app.exec()