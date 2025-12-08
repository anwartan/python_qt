from PyQt6.uic import loadUi  
from PyQt6.QtWidgets import QInputDialog
from polars import Date
from sympy import false
from egg_counter.egg_service import Eggservice
from PyQt6.QtWidgets import QMessageBox, QMainWindow
from datetime import datetime
class EggCounter(QMainWindow):
     def __init__(self):
          super().__init__()
          loadUi('egg_counter/counter.ui', self) 
          self.tambah_data_button.clicked.connect(self.clicked_tambah)
          self.edit_data_button.clicked.connect(self.clicked_edit)
          self.hapus_data_button.clicked.connect(self.clicked_hapus)
          self.import_data_button.clicked.connect(self.clicked_import)
          self.export_data_button.clicked.connect(self.clicked_export)
          self.eggservice = Eggservice()
     def clicked_tambah(self):
        tanggal, ok1 = QInputDialog.getText(self, 'add tanggal', 'tanggal:(YYYY-MM-DD)')
        if ok1:
          py_date = datetime.strptime(tanggal, "%Y-%m-%d").date() 
        elif ok1 == False:         
          return
        tipe, ok2 = QInputDialog.getText(self, 'add tipe', 'tipe:')
        if ok2 == False:
            return
        jumlah_telur, ok3 = QInputDialog.getText(self, 'add jumlah telur', 'jumlah_telur:')
        if ok3 == False:
            return
        telur_rusak, ok4 = QInputDialog.getText(self, 'telur rusak', 'jumlah_telur_rusak:')
        if ok4 == False:
            return
        self.eggservice.add_counter(py_date, tipe, jumlah_telur, telur_rusak)
        self.clicked_edit()
     def clicked_edit(self):
        current_row = self.eggwidget.currentRow()
        egg_id = self.eggwidget.item(current_row, 0)
        print(egg_id)
        tanggal, ok1 = QInputDialog.getText(self, 'add tanggal', 'Date')
        if ok1 == False:
            return
        tipe, ok2 = QInputDialog.getText(self, 'add tipe', 'tipe:')
        if ok2 == False:
            return
        jumlah_telur, ok3 = QInputDialog.getText(self, 'add jumlah telur', 'jumlah_telur:')
        if ok3 == False:
            return
        telur_rusak, ok4 = QInputDialog.getText(self, 'telur rusak', 'jumlah_telur_rusak:')
        if ok4 == False:
            return
        self.eggservice.add_counter(tanggal, tipe, jumlah_telur, telur_rusak)
        self.clicked_edit()
     def clicked_hapus(self):
        comment = QMessageBox.question(self, 'Delete Account', 'Are you sure you want to delete this account?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        current_row = self.tableWidget.currentRow()
        id = int(self.tableWidget.item(current_row, 0))
        if comment == QMessageBox.StandardButton.Yes:
            self.accountservice.delete_password(id)
        else:
            print("no")
        self.clicked_search()
     def clicked_import(self):     
        pass
     def clicked_export(self):
        pass