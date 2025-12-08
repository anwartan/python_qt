import json
from unittest.loader import VALID_MODULE_NAME
from PyQt6.uic import loadUi
from sympy import Q
from torch import layout
from api_client import Apiclient
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCharts import QChart, QCandlestickSeries, QCandlestickSet, QChartView, QDateTimeAxis, QValueAxis
from PyQt6.QtCore import Qt, QDateTime
import pandas as pd
COIN_MAP = {
    "BTCUSDT": "bitcoin",
    "ETHUSDT": "ethereum",
    "BNBUSDT": "binance Coin",
}
class CryptoTrading(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("crypto/crypto.ui", self)
        self.chart = QChart()
        self.chart_view = QChartView(self.chart)
        layout = QVBoxLayout(self.chartwidget)
        layout.addWidget(self.chart_view)
        self.api_client = Apiclient()
        self.api_client.signal_finished.connect(self.on_data_received)
        self.comboBox.addItems(self.combo_box_items())
        self.comboBoxs.addItems(self.combo_boxs_item())
        self.load_button.clicked.connect(self.on_load_button)

    def combo_box_items(self):
        return COIN_MAP.keys()
    def combo_boxs_item(self):
        return ["1", "7", "14", "30", "90", "180", "365", "max"]
    def on_load_button(self):
        coin = COIN_MAP[self.comboBox.currentText()]
        time = self.comboBoxs.currentText()
        API_URL = f"https://api.coingecko.com/api/v3/coins/{coin}/ohlc?vs_currency=usd&days={time}"
        self.api_client.get(API_URL)
    def on_data_received(self, data):
        converted_data = json.loads(data)
        dt = pd.DataFrame(converted_data, columns=["timestamp", "open", "high", "low", "close"])
        self.graphics(dt)
    def graphics(self, data):
        if data.empty:
            return
        self.chart.removeAllSeries()
        for i in self.chart.axes():
            self.chart.removeAxis(i)
        series = QCandlestickSeries()
        series.setIncreasingColor(Qt.GlobalColor.green)
        series.setDecreasingColor(Qt.GlobalColor.red)
        print(data)
        for index, row in data.iterrows():
            series.append(
                QCandlestickSet(
                    float(row["open"]),
                    float(row["high"]),
                    float(row["low"]),
                    float(row["close"]), 
                    int(row["timestamp"])  
                )
            )
        self.chart.addSeries(series)
        
        datetime = QDateTimeAxis()
        datetime.setFormat("yyyy-MM-dd")
        datetime.setTitleText("date time")
        self.chart.addAxis(datetime, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(datetime)
        startdate = data["timestamp"].min()
        enddate = data["timestamp"].max()
        datetime.setRange(
            QDateTime.fromMSecsSinceEpoch(int(startdate)),
            QDateTime.fromMSecsSinceEpoch(int(enddate)),
        )
        value = QValueAxis()
        value.setTitleText("price (USD)")
        self.chart.addAxis(value, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(value)
        minprice = data["low"].min()
        maxprice = data["high"].max()
        value.setRange(minprice, maxprice)