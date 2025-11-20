import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QCheckBox, QListWidget
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt
import json
class Todoapp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("todo/todo.ui", self)
        self.tambah.clicked.connect(self.tambah_tugas)
        self.hapus.clicked.connect(self.hapus_tugas)
        self.load_data()
    def tambah_tugas(self):
        inputan = self.input.toPlainText()
        if inputan:
            item = QListWidgetItem(inputan)
            item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            item.setCheckState(Qt.CheckState.Unchecked)         
            self.listWidget.addItem(item)
            self.listWidget.addItem(item)
            self.input.clear()
            self.save_data()
    def hapus_tugas(self):
        checked_items = []
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                checked_items.append(i)
        for i in checked_items:
            item=   self.listWidget.item(i)
            row = self.listWidget.row(item)
            self.listWidget.takeItem(row)
        self.save_data()

       
    def save_data(self):
        data = []
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            data.append({
                "text": item.text(),
                "checked": item.checkState() == Qt.CheckState.Checked
            })

        with open("todo_data.json", "w") as f:
            json.dump(data, f, indent=4)
    def load_data(self):
        try:
            with open("todo_data.json", "r") as f:
                data = json.load(f)

            for entry in data:
                item = QListWidgetItem(entry["text"])
                item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                item.setCheckState(Qt.CheckState.Checked if entry["checked"] else Qt.CheckState.Unchecked)
                self.listWidget.addItem(item)

        except FileNotFoundError:
            pass 

