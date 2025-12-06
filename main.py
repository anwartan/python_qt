from PyQt6.QtWidgets import  QMainWindow, QApplication
from PyQt6.uic import loadUi
import sys
from telur.TelurWidget import TelurWidget
from map.map import MapWidget
from cuaca.Weather import Weather
from telur.TelurWidget import TelurWidget
from passwordmanager.manager import PasswordWidget
from todo.todo_app import Todoapp
from chartt.chart import ChartWindow
from currency.currency import Money
from eggcounter.egg import Eggcounterwidget
from cyrpto.cyrpto import CyrptoWindow
from passwordmanager.manager import PasswordWidget
>>>>>>> e0cce20fb142012ca7cb74c9c4bc626a76db0ca6
class MainWindow(QMainWindow):
   def __init__(self):
        super().__init__()
        loadUi("main.ui",self)
        self.listWidget.itemDoubleClicked.connect(self.on_item_dobel_clicked)
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
        elif item.text() == "todoapp":
                self.todo_app= Todoapp()
                self.todo_app.show()
        elif item.text() == "chart":
                self.chart_window = ChartWindow()
                self.chart_window.show()
        elif item.text() == "currrency converter":
                self.currency_window = Money()
                self.currency_window.show()
        elif item.text() == "Cyrpto ":
                self.cyrpto_window = CyrptoWindow()
                self.cyrpto_window.show()
        elif item.text() == "Egg counter":
                self.egg_window = Eggcounterwidget()
                self.egg_window.show()

app = QApplication(sys.argv)


win = MainWindow()
win.show()


app.exec()