import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QBarSeries, QBarSet, QPieSeries
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt


class ChartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Charts Example")
        self.setGeometry(200, 100, 1200, 700)

        # Layout utama
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.layout = QVBoxLayout(main_widget)

        # Tombol Chart
        button_layout = QHBoxLayout()
        self.layout.addLayout(button_layout)

        self.btn_line = QPushButton("Line Chart")
        self.btn_bar = QPushButton("Bar Chart")
        self.btn_pie = QPushButton("Pie Chart")

        button_layout.addWidget(self.btn_line)
        button_layout.addWidget(self.btn_bar)
        button_layout.addWidget(self.btn_pie)

        self.btn_line.clicked.connect(self.show_line_chart)
        self.btn_bar.clicked.connect(self.show_bar_chart)
        self.btn_pie.clicked.connect(self.show_pie_chart)

        # Area chart
        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.layout.addWidget(self.chart_view)

        self.show_line_chart()

    # ================== LINE CHART ====================
    def show_line_chart(self):
        series = QLineSeries()
        series.append(1, 1)
        series.append(2, 2)
        series.append(3, 3)
        series.append(4, 4)
        series.append(5, 5)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Line Chart Example")
        chart.createDefaultAxes()

        self.chart_view.setChart(chart)

    # ================== BAR CHART ====================
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

    # ================== PIE CHART ====================
    def show_pie_chart(self):
        series = QPieSeries()
        series.append("A", 40)
        series.append("B", 30)
        series.append("C", 20)
        series.append("D", 10)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Pie Chart Example")

        self.chart_view.setChart(chart)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChartWindow()
    window.show()
    sys.exit(app.exec())