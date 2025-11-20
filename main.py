from PyQt6.QtWidgets import  QMainWindow, QApplication
from PyQt6.uic import loadUi
import sys
from telur.TelurWidget import TelurWidget
from map.map import MapWidget
from cuaca.Weather import Weather
from telur.TelurWidget import TelurWidget
from passwordmanager.password import password_manager_widget
from todo.todo_app import Todoapp
from chartt.chart import ChartWindow
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
              self.password_window = password_manager_widget()
              self.password_window.show()
        elif item.text() == "todoapp":
                self.todo_app= Todoapp()
                self.todo_app.show()
        elif item.text() == "chart":
                self.chart_window = ChartWindow()
                self.chart_window.show()
app = QApplication(sys.argv)


win = MainWindow()
win.show()


app.exec()