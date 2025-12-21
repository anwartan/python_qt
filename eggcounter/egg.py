from PyQt6.QtWidgets import QMainWindow, QInputDialog, QTableWidgetItem, QMessageBox, QFileDialog, QWidget, QVBoxLayout
from PyQt6.uic import loadUi
from PyQt6.QtCore import QDate, QDateTime, QTime, Qt
from eggcounter.service.eggservice import Eggservice
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QDateTimeAxis, QValueAxis
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import QPointF
import csv
import datetime


class Eggcounterwidget(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('eggcounter/counter.ui', self)

        self.eggservice = Eggservice()
        self.mode_tabel = True

        self.graph_container = QWidget(self)
        self.graph_layout = QVBoxLayout()
        self.graph_container.setLayout(self.graph_layout)
        self.graph_container.setGeometry(0, 30, 600, 430)
        self.graph_container.hide()

        self.tambah.clicked.connect(self.tamabahtelur)
        self.Edit.clicked.connect(self.edittelur)
        self.hapus.clicked.connect(self.hapustelur)
        self.import_2.clicked.connect(self.importdata)
        self.export_2.clicked.connect(self.exportdata)
        self.tabel.clicked.connect(self.toggle_view)

        self.load_data()

    def tamabahtelur(self):
        tanggal, ok1 = QInputDialog.getText(self, 'telur', 'Masukan tanggal (YYYY-MM-DD):')
        if not ok1:
            return
        try:
            tanggal = datetime.date.fromisoformat(tanggal)
        except:
            QMessageBox.warning(self, "Error", "Format tanggal salah!")
            return

        tipe, ok2 = QInputDialog.getText(self, 'telur', 'Type telur:')
        if not ok2:
            return

        jumlah, ok3 = QInputDialog.getInt(self, 'telur', 'jumlah telur:')
        if not ok3:
            return

        rusak, ok4 = QInputDialog.getInt(self, 'telur', 'Telur rusak:')
        if not ok4:
            return

        self.eggservice.add(tanggal, tipe, jumlah, rusak)
        self.load_data()

    def edittelur(self):
        row = self.tableWidget.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Warning", "Select row first.")
            return

        id = int(self.tableWidget.item(row, 0).text())
        tanggal = self.tableWidget.item(row, 1).text()
        tipe = self.tableWidget.item(row, 2).text()
        jumlah = self.tableWidget.item(row, 3).text()
        rusak = self.tableWidget.item(row, 4).text()

        tanggal, ok1 = QInputDialog.getText(self, 'Edit', 'Tanggal:', text=tanggal)
        if not ok1:
            return
        try:
            tanggal = datetime.date.fromisoformat(tanggal)
        except:
            QMessageBox.warning(self, "Error", "Format tanggal salah!")
            return

        tipe, ok2 = QInputDialog.getText(self, 'Edit', 'Type:', text=tipe)
        if not ok2:
            return

        jumlah, ok3 = QInputDialog.getInt(self, 'Edit', 'Jumlah:', int(jumlah))
        if not ok3:
            return

        rusak, ok4 = QInputDialog.getInt(self, 'Edit', 'Rusak:', int(rusak))
        if not ok4:
            return

        self.eggservice.edit(id, tanggal, tipe, jumlah, rusak)
        self.load_data()

    def hapustelur(self):
        row = self.tableWidget.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Warning", "Select row first.")
            return

        id = int(self.tableWidget.item(row, 0).text())
        q = QMessageBox.question(self, "Confirm", "Delete data?")
        if q != QMessageBox.StandardButton.Yes:
            return

        self.eggservice.delete(id)
        self.load_data()

    def importdata(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "CSV Files (*.csv)")
        if not path:
            return
        imported = 0
        try:
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if len(row) < 4:
                        continue
                    t, tipe, j, r = row
                    t = datetime.date.fromisoformat(t)
                    self.eggservice.add(t, tipe, int(j), int(r))
                    imported += 1
            QMessageBox.information(self, "Success", f"Imported {imported} data!")
            self.load_data()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
    def exportdata(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "CSV Files (*.csv)")
        if not path:
            return

        try:
            eggs = self.eggservice.getall()
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["tanggal", "type", "jumlah", "rusak"])
                for egg in eggs:
                    w.writerow([egg.tanggal, egg.type, egg.jumlah, egg.rusak])

            QMessageBox.information(self, "Success", "Export complete!")

        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def load_data(self):
        if self.mode_tabel:
            self.graph_container.hide()
            self.tableWidget.show()

            eggs = self.eggservice.getall()
            self.tableWidget.setColumnCount(5)
            self.tableWidget.setHorizontalHeaderLabels(["ID", "Tanggal", "Type", "Jumlah", "Rusak"])
            self.tableWidget.setRowCount(len(eggs))

            for row, egg in enumerate(eggs):
                self.tableWidget.setItem(row, 0, QTableWidgetItem(str(egg.id)))
                self.tableWidget.setItem(row, 1, QTableWidgetItem(str(egg.tanggal)))
                self.tableWidget.setItem(row, 2, QTableWidgetItem(str(egg.type)))
                self.tableWidget.setItem(row, 3, QTableWidgetItem(str(egg.jumlah)))
                self.tableWidget.setItem(row, 4, QTableWidgetItem(str(egg.rusak)))

        else:
            self.tableWidget.hide()
            self.graph_container.show()
            self.render_chart()

    def render_chart(self):
        for i in reversed(range(self.graph_layout.count())):
            self.graph_layout.itemAt(i).widget().deleteLater()

        chart = QChart()
        chart.setTitle("Analisis Produksi Telur Harian")

        series_jumlah = QLineSeries()
        series_jumlah.setName("Jumlah Telur")

        series_rusak = QLineSeries()
        series_rusak.setName("Telur Rusak")
        series_rusak.setColor(Qt.GlobalColor.red)

        eggs = self.eggservice.getall()
        eggs.sort(key=lambda x: x.tanggal)

        for egg in eggs:
            t = egg.tanggal
            qdt = QDateTime(QDate(t.year, t.month, t.day), QTime(0, 0))
            ts = qdt.toMSecsSinceEpoch()
            series_jumlah.append(ts, egg.jumlah)
            series_rusak.append(ts, egg.rusak)

        chart.addSeries(series_jumlah)
        chart.addSeries(series_rusak)

        ax = QDateTimeAxis()
        ax.setFormat("dd MMM yyyy")
        ax.setTitleText("Tanggal")
        chart.addAxis(ax, Qt.AlignmentFlag.AlignBottom)
        series_jumlah.attachAxis(ax)
        series_rusak.attachAxis(ax)

        ay = QValueAxis()
        ay.setTitleText("Jumlah Telur Total")
        chart.addAxis(ay, Qt.AlignmentFlag.AlignLeft)
        series_jumlah.attachAxis(ay)
        series_rusak.attachAxis(ay)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignTop)

        view = QChartView(chart)
        view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.graph_layout.addWidget(view)

    def toggle_view(self):
        self.mode_tabel = not self.mode_tabel
        self.tabel.setText("Grafik" if self.mode_tabel else "Tabel")
        self.load_data()




def render_chart(self):
        for i in reversed(range(self.graph_layout.count())):
            self.graph_layout.itemAt(i).widget().deleteLater()

        chart = QChart()
        series = QLineSeries()
        eggs = self.eggservice.getall()
        eggs.sort(key=lambda x: x.tanggal)

        for egg in eggs:
            t = egg.tanggal
            qdt = QDateTime(QDate(t.year, t.month, t.day), QTime(0, 0))
            ts = qdt.toMSecsSinceEpoch()
            series.append(QPointF(ts, egg.jumlah))

        chart.addSeries(series)

        ax = QDateTimeAxis()
        ax.setFormat("yyyy-MM-dd")
        chart.addAxis(ax, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(ax)

        ay = QValueAxis()
        chart.addAxis(ay, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(ay)

        view = QChartView(chart)
        view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.graph_layout.addWidget(view)


