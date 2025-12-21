from PyQt6.QtWidgets import QMainWindow, QApplication, QVBoxLayout
from PyQt6.uic import loadUi
from api_client import Apiclient
from PyQt6.QtCharts import QChart, QChartView, QCandlestickSeries, QCandlestickSet, QDateTimeAxis, QValueAxis
from PyQt6.QtCore import Qt, QDateTime
import json
import pandas as pd

COIN_MAP = {
    "BTCUSDT": "bitcoin",
    "ETHUSDT": "ethereum",
    "BNBUSDT": "binancecoin"
}

TimeFrame = ["1"," 7", "14", "30", "90", "180", "365", "max"]


class CyrptoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("cyrpto/cyrpto.ui", self)

        self.api_client = Apiclient()
        self.chart = QChart()
        self.chart_view = QChartView(self.chart)

        layout = QVBoxLayout(self.chartWidget)
        layout.addWidget(self.chart_view)

        self.loadButton.clicked.connect(self.on_load_chart)
        self.api_client.signal_finished.connect(self.on_success)

        self.coinComboBox.addItems(list(COIN_MAP.keys()))
        self.timeframeComboBox.addItems(TimeFrame)

    def on_load_chart(self):
        coin = COIN_MAP[self.coinComboBox.currentText()]
        timeframe = self.timeframeComboBox.currentText()

        # Coingecko API OHLC
        api_url = f"https://api.coingecko.com/api/v3/coins/{coin}/ohlc?vs_currency=usd&days={timeframe}"
        self.api_client.get(api_url)

    def on_success(self, response):
        # response is TEXT not FILE
        convert_data = json.loads(response)

        df = pd.DataFrame(convert_data, columns=["timestamp", "open", "high", "low", "close"])
        self.draw_candlestick(df)

    def draw_candlestick(self, data: pd.DataFrame):
        if data.empty:
            return

        # Clean chart
        self.chart.removeAllSeries()
        for axis in self.chart.axes():
            self.chart.removeAxis(axis)

        series = QCandlestickSeries()
        series.setIncreasingColor(Qt.GlobalColor.green)
        series.setDecreasingColor(Qt.GlobalColor.red)

        # Add candles
        for _, row in data.iterrows():
            candle = QCandlestickSet(
                float(row['open']),
                float(row['high']),
                float(row['low']),
                float(row['close']),
                int(row['timestamp']) / 1000  # convert ms → seconds
            )
            series.append(candle)

        self.chart.addSeries(series)
        self.chart.createDefaultAxes()
        # X Axis (DateTime)
        axis_x = QDateTimeAxis()
        axis_x.setFormat("yyyy-MM-dd HH:mm")
        axis_x.setTitleText("Date")
        self.chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)

        axis_x.setRange(
            QDateTime.fromMSecsSinceEpoch(int(data['timestamp'].min())),
            QDateTime.fromMSecsSinceEpoch(int(data['timestamp'].max()))
        )

        # Y Axis (Price)
        axis_y = QValueAxis()
        axis_y.setTitleText("Price (USD)")
        self.chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)

        axis_y.setRange(
            float(data['low'].min()),
            float(data['high'].max())
        )

        self.chart.setTitle(f"Candlestick — {self.coinComboBox.currentText()} ({self.timeframeComboBox.currentText()} days)")
        self.chart_view.setChart(self.chart)

