import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QTabWidget
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QBarSeries, QBarSet, QPieSeries
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt


class ChartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Charts Example")
        self.setGeometry(200, 100, 1200, 700)
        tab_widget = QTabWidget()
        tab_widget.addTab(self.generate_bar_chart(), "Bar Chart")
        tab_widget.addTab(self.generate_pie_chart(), "Pie Chart")
        self.setCentralWidget(tab_widget)
        
        # main_widget = QWidget()
        # self.setCentralWidget(main_widget)
        # self.layout = QVBoxLayout(main_widget)
        # button_layout = QHBoxLayout()
        # self.layout.addLayout(button_layout)
        # self.btn_bar = QPushButton("Bar Chart")
        # self.btn_pie = QPushButton("Pie Chart")
        # button_layout.addWidget(self.btn_bar)
        # button_layout.addWidget(self.btn_pie)

        # self.btn_bar.clicked.connect(self.show_bar_chart)
        # self.btn_pie.clicked.connect(self.show_pie_chart)
        # self.chart_view = QChartView()
        # self.layout.addWidget(self.chart_view)
        
    def generate_bar_chart(self):
        set1 = QBarSet("Series 1")
        set2 = QBarSet("Series 2")

        set1 << 1 << 2 << 3 << 4 << 5
        set2 << 5 << 0 << 0 << 4 << 3

        series = QBarSeries()
        series.append(set1)
        series.append(set2)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Bar Chart")
        chart.createDefaultAxes()
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignTop)

        chart_view = QChartView(chart)

        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(chart_view)
        tab.setLayout(layout)
        return tab
        
    def show_bar_chart(self):
        set1 = QBarSet("Series 1")
        set2 = QBarSet("Series 2")

        set1 << 1 << 2 << 3 << 4 << 5
        set2 << 5 << 0 << 0 << 4 << 3

        series = QBarSeries()
        series.append(set1)
        series.append(set2)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Bar Chart")
        chart.createDefaultAxes()
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignTop)

        self.chart_view.setChart(chart)

    def generate_pie_chart(self):
        series = QPieSeries()
        series.append("Apples", 40)
        series.append("Banana", 30)
        series.append("Cherries", 20)
        series.append("Dates", 10)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Pie Chart")

        chart_view = QChartView(chart)
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(chart_view)
        tab.setLayout(layout)
        return tab
    def show_pie_chart(self):
        series = QPieSeries()
        series.append("Apples", 40)
        series.append("Banana", 30)
        series.append("Cherries", 20)
        series.append("Dates", 10)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Pie Chart")

        self.chart_view.setChart(chart)

