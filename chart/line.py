import sys
from PyQt6.QtWidgets import  QMainWindow, QApplication, QTabWidget, QVBoxLayout, QWidget
from PyQt6.QtCharts import QChart, QChartView, QLineSeries,    QPieSeries
from PyQt6.QtCore import QPointF,   Qt
from PyQt6.QtGui import QPainter, QPen, QColor
class Charts(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Line Chart PyQt6")
        tabs = QTabWidget()
        tabs.addTab(self.setup_chart(), "line chart")
        tabs.addTab(self.pie_chart(), "pie chart")
        self.resize(600, 400)
        self.setCentralWidget(tabs)


    def setup_chart(self):
        series = QLineSeries()
        for x, y in [(0, 1), (1.5, 3),(2.5, 4),(4, 1), (5, 5)]:
            series.append(QPointF(x, y))
        series.setColor(Qt.GlobalColor.red)
        series.setName("merah")
        series2 = QLineSeries()
        for x, y in [(0, 1), (1.5, 3),(5, 4),(4, 1), (4, 5)]:
            series2.append(QPointF(x, y))
        series2.setColor(Qt.GlobalColor.green)
        series2.setName("hijau")
        series3 = QLineSeries()
        for x, y in [(0, 1), (2, 3),(2, 4),(4, 1), (5, 5)]:
            series3.append(QPointF(x, y))
        series3.setColor(Qt.GlobalColor.blue)
        series3.setName("Biru")
        chart = QChart()
        chart.addSeries(series)
        chart.addSeries(series2)
        chart.addSeries(series3)
        chart.setTitle("Contoh Line Chart")
        chart.createDefaultAxes()
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(chart_view)
        tab.setLayout(layout)
        return tab
    def pie_chart(self):
        series = QPieSeries()
        series.append("Apples", 1000)
        series.append("Bananas", 30)
        series.append("Cherries", 20)
        series.append("Dates", 10)

        for s in series.slices():
            s.setLabelVisible(False)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Pie Chart")

        view = QChartView(chart)
        view.setRenderHint(QPainter.RenderHint.Antialiasing)
        view.resize(600, 500)
        view.show()

        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(view)
        tab.setLayout(layout)
        return tab

