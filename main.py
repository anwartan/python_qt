from PyQt6.QtWidgets import  QMainWindow, QApplication
from PyQt6.uic import loadUi
import sys
from cuaca.Weather import Weather
from telur.TelurWidget import TelurWidget
class MainWindow(QMainWindow):
   def __init__(self):
        super().__init__()
        loadUi("main.ui",self)
        self.listWidget.itemDoubleClicked.connect(self.on_item_double_clicked)
   def on_item_double_clicked(self,item):
        if item.text() == "telur":
            self.telur_window = TelurWidget()
            self.telur_window.show()
        elif item.text() == "cuaca":
            self.cuaca_window = Weather()
            self.cuaca_window.show()

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()