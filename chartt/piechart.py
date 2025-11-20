import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

class PieChartApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Matplotlib Pie Chart")
        self.setGeometry(120, 100, 800, 900)  # (x, y, lebar, tinggi)

        # Widget utama dan tata letak
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Buat canvas Matplotlib
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.ax.set_title("Pie Chart")
        self.draw_pie_chart()
    def draw_pie_chart(self):
        labels = ['Apples', 'Bananas', 'Cherries', 'Dates']
        sizes = [40, 30, 15, 15]
        colors = ['#B0E0E6', '#0099CC', "#0093DD", '#003366']

        self.ax.clear()

   
        wedges, texts = self.ax.pie(
            sizes,
            colors=colors,
            startangle=90,  
            wedgeprops={'linewidth': 0} 
        )

        # Tambahkan legenda
        self.ax.set_title("Pie Chart")
        self.ax.legend(
            wedges,
            labels,
            loc="upper center",
            bbox_to_anchor=(0.5, 1.1),
            ncol=len(labels),
            frameon=False 
        )
        self.ax.axis('equal')
        self.canvas.draw()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    pie_chart_app = PieChartApp()
    pie_chart_app.show()
    sys.exit(app.exec())