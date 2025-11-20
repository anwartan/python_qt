from PyQt6.QtWidgets import  QMainWindow, QApplication
from PyQt6.uic import loadUi
import sys
from telur.TelurWidget import TelurWidget
from map.map import MapWidget
from cuaca.Weather import Weather
from telur.TelurWidget import TelurWidget
from currency.currency import Money
from chart.line import Charts
from passwordmanager.manager import PasswordWidget
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
        elif item.text() == "cuaca":
                self.cuaca_window = Weather()
                self.cuaca_window.show()
        elif item.text() == "password manager":
                self.password_window = PasswordWidget()
                self.password_window.show()
        elif item.text() == "currrency converter":
                self.currency_window = Money()
                self.currency_window.show()
        elif item.text() == "diagram":
                self.diagram_window = Charts()
                self.diagram_window.show()

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()