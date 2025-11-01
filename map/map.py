import sys
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QPixmap
import requests
from PyQt6.QtCore import Qt
class MapWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('map/map.ui', self)
        self.latitude_spinbox.setFocus (Qt.FocusReason.OtherFocusReason)
        self.latitude_spinbox.selectAll()
        self.api_key = "AIzaSyDpmaYZeO7WOFWkcIeC3Ej-Y5dDa1FDxZs"
        self.pushButton.clicked.connect(self.load_map)
    
    def load_map(self):
        lat = self.latitude_spinbox.value()
        lon = self.long_spinbox.value()
        url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom=14&size=600x400&maptype=roadmap&markers=color:red%7C{lat},{lon}&key=AIzaSyDpmaYZeO7WOFWkcIeC3Ej-Y5dDa1FDxZs"
        print(url)
        response = requests.get(url)
        if response.status_code == 200:
            binary_body = response.content
            pixmap = QPixmap()
            pixmap.loadFromData(binary_body)
            self.label_2.setPixmap(pixmap)
        else:
            print("Error loading map:", response.status_code)