from PyQt6.QtWidgets import QWidget
from PyQt6.uic import loadUi
from api_client import Apiclient
import json
class Money(QWidget):
    def __init__(self):
        super ().__init__()
        loadUi("currency/currency.ui", self)
        self.api_client = Apiclient()
        self.comboBox.addItems(self.combo_box_items())
        self.combos_Box.addItems(self.a_box_items()) 
        self.konversi_button.clicked.connect(self.on_konvert_button)
        self.api_client.signal_finished.connect(self.get_data_received)
    def combo_box_items (self):
        return ["USD", "IDR", "JPY", "EUR", "MYR", "CNY", "GBP", "AUD", "PHP", "INR", "IRR", "QAR", "LKR", "CHF", "THB", "AED", "ZWD", "DZD", "ARS", "BDT", "BRL", "CLP", "KHR", "MGA"]
    
    def a_box_items (self):
        return ["USD", "IDR", "JPY", "EUR", "MYR", "CNY", "GBP", "AUD", "PHP", "INR", "IRR", "QAR", "LKR", "CHF", "THB", "AED", "ZWD", "DZD", "ARS", "BDT", "BRL", "CLP", "KHR", "MGA"]
    def on_konvert_button (self):
        nilai = int(self.input_nilai.text())
        dari = self.comboBox.currentText()
        ke = self.combos_Box.currentText()
        API_URL = f"https://free.ratesdb.com/v1/rates?from={dari}&to={ke}"
        self.api_client.get(API_URL)
    def get_data_received(self, get):
        nilai = int(self.input_nilai.text())
        ke = self.combos_Box.currentText()
        get = json.loads(get)
        dapat = float(get["data"]["rates"][ke])*nilai
        dapat_string = str(dapat) + " " + str(ke)
        tanggal = " " + str(get["data"]["date"])
        self.hasil_value.setText(str(dapat_string))
        self.tanggal_value.setText(tanggal)
