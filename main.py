from PyQt6.QtWidgets import  QMainWindow, QApplication
from PyQt6.uic import loadUi
import sys
from telur.TelurWidget import TelurWidget
from map.map import MapWidget
class MainWindow(QMainWindow):
   def __init__(self):
        super().__init__()
        loadUi("main.ui",self)
        self.listWidget.itemDoubleClicked.connect (self.on_item_dobel_clicked)
   def on_item_dobel_clicked(self,item):
        if item.text() == "telur":
                self.telur_window = TelurWidget()
                self.telur_window.show()
        elif item.text() == "map":
                self.map_window = MapWidget()
                self.map_window.show()
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()