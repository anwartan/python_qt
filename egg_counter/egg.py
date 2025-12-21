from PyQt6.uic import loadUi  
from PyQt6.QtWidgets import QInputDialog, QTableWidgetItem, QFileDialog, QMessageBox, QMainWindow
from datetime import datetime
import csv
from egg_counter.egg_service import Eggservice
from database.db_session import sessionlocal
from database.entity.counter import Counter
from database.entity.egg import Egg
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QDateTimeAxis, QValueAxis
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPen, QColor, QPainter
from PyQt6 import QtWidgets, uic
import pandas as pd
class EggCounter(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('egg_counter/counter.ui', self)

        # Connect signals
        self.tambah_data_button.clicked.connect(self.clicked_tambah)
        self.edit_data_button.clicked.connect(self.clicked_edit)
        self.hapus_data_button.clicked.connect(self.clicked_hapus)
        self.import_data_button.clicked.connect(self.clicked_import)
        self.export_data_button.clicked.connect(self.clicked_export)
        self.grafik_button.clicked.connect(self.clicked_grafik)
        self.eggservice = Eggservice()
        self.load_data()

    def clicked_tambah(self):
        tanggal, ok1 = QInputDialog.getText(self, 'add tanggal', 'tanggal:(YYYY-MM-DD)')
        if not ok1:
            return
        try:
            py_date = datetime.strptime(tanggal, "%Y-%m-%d").date()
        except Exception:
            QMessageBox.warning(self, "Error", "Format tanggal salah! Gunakan YYYY-MM-DD")
            return

        tipe, ok2 = QInputDialog.getText(self, 'add tipe', 'type:')
        if not ok2:
            return

        jumlah_telur, ok3 = QInputDialog.getInt(self, 'add jumlah telur', 'jumlah:')
        if not ok3:
            return

        telur_rusak, ok4 = QInputDialog.getInt(self, 'telur rusak', 'rusak:')
        if not ok4:
            return

        self.eggservice.add_counter(py_date, tipe, int(jumlah_telur), int(telur_rusak))
        self.load_data()

    def clicked_edit(self):
        current_row = self.eggwidget.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Select row first.")
            return

        try:
            egg_id = int(self.eggwidget.item(current_row, 0).text())
        except Exception:
            QMessageBox.warning(self, "Error", "Invalid ID selected.")
            return

        curr_tanggal = self.eggwidget.item(current_row, 1).text()
        curr_tipe = self.eggwidget.item(current_row, 2).text()
        curr_jumlah = int(self.eggwidget.item(current_row, 3).text())
        curr_rusak = int(self.eggwidget.item(current_row, 4).text())

        tanggal, ok1 = QInputDialog.getText(self, 'Edit tanggal', 'tanggal:(YYYY-MM-DD)', text=curr_tanggal)
        if not ok1:
            return
        try:
            py_date = datetime.strptime(tanggal, "%Y-%m-%d").date()
        except Exception:
            QMessageBox.warning(self, "Error", "Format tanggal salah! Gunakan YYYY-MM-DD")
            return

        tipe, ok2 = QInputDialog.getText(self, 'Edit tipe', 'type:', text=curr_tipe)
        if not ok2:
            return

        jumlah_telur, ok3 = QInputDialog.getInt(self, 'Edit jumlah telur', 'jumlah:', curr_jumlah)
        if not ok3:
            return

        telur_rusak, ok4 = QInputDialog.getInt(self, 'Edit telur rusak', 'rusak:', curr_rusak)
        if not ok4:
            return

        self.eggservice.edit_counter(egg_id, py_date, tipe, int(jumlah_telur), int(telur_rusak))
        self.load_data()

    def clicked_hapus(self):
        current_row = self.eggwidget.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Select row first.")
            return

        try:
            id = int(self.eggwidget.item(current_row, 0).text())
        except Exception:
            QMessageBox.warning(self, "Error", "Invalid ID selected.")
            return

        q = QMessageBox.question(self, "Confirm", "Delete data?")
        if q != QMessageBox.StandardButton.Yes:
            return

        self.eggservice.delete_counter(id)
        self.load_data()

    def load_data(self):
        records = []
        with sessionlocal() as session:
            counters = session.query(Counter).all()
            eggs = session.query(Egg).all()
        for c in counters:
            records.append({
                'id': c.id,
                'tanggal': c.tanggal,
                'tipe': c.tipe,
                'jumlah': c.jumlah_telur,
                'rusak': c.jumlah_telur_rusak,
                'source': 'counter'
            })

        # Normalize Egg records
        for e in eggs:
            records.append({
                'id': e.id,
                'tanggal': e.tanggal,
                'tipe': getattr(e, 'type', getattr(e, 'tipe', '')),
                'jumlah': getattr(e, 'jumlah', None) or getattr(e, 'jumlah_telur', None) or 0,
                'rusak': getattr(e, 'rusak', None) or getattr(e, 'jumlah_telur_rusak', None) or 0,
                'source': 'egg'
            })

        # Sort by date
        records.sort(key=lambda r: r['tanggal'])

        self.eggwidget.setColumnCount(5)
        self.eggwidget.setHorizontalHeaderLabels(["ID", "Tanggal", "Tipe", "Jumlah", "Rusak"])
        self.eggwidget.setRowCount(len(records))

        for i, rec in enumerate(records):
            self.eggwidget.setItem(i, 0, QTableWidgetItem(str(rec['id'])))
            self.eggwidget.setItem(i, 1, QTableWidgetItem(str(rec['tanggal'])))
            self.eggwidget.setItem(i, 2, QTableWidgetItem(str(rec['tipe'])))
            self.eggwidget.setItem(i, 3, QTableWidgetItem(str(rec['jumlah'])))
            self.eggwidget.setItem(i, 4, QTableWidgetItem(str(rec['rusak'])))

    def clicked_import(self):
        path, _ = QFileDialog.getOpenFileName(self, "Import CSV", "", "CSV Files (*.csv);;All Files(*)")
        if not path:
            return
        imported = 0
        try:
            with open(path, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader, None)
                for row in reader:
                    if len(row) < 4:
                        continue
                    t, tipe, j, r = row
                    try:
                        t = datetime.strptime(t, "%Y-%m-%d").date()
                        j = int(j)
                        r = int(r)
                    except Exception:
                        continue
                    self.eggservice.add_counter(t, tipe, j, r)
                    imported += 1
            QMessageBox.information(self, "Success", f"Imported {imported} data!")
            self.load_data()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def clicked_export(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save File", "egg_export.csv", "CSV Files (*.csv);;All Files(*)")
        if not path:
            return
        try:
            accounts = self.eggservice.get_all()
            with open(path, 'w', newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'tanggal', 'tipe', 'jumlah_telur', 'jumlah_telur_rusak'])
                for acc in accounts:
                    writer.writerow([acc.id, acc.tanggal, acc.tipe, acc.jumlah_telur, acc.jumlah_telur_rusak])
            QMessageBox.information(self, "Success", "Export complete!")
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
    def update_graph(self):

        if not self.eggwidget.layout():
            self.chart_layout = QtWidgets.QVBoxLayout(self.eggwidget)
        else:
            self.chart_layout = self.eggwidget.layout()
        while self.chart_layout.count():
            child = self.chart_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        with sessionlocal() as session:
            records = session.query(Counter).order_by(Counter.tanggal).all()
        
        if not records:
            return

        df = pd.DataFrame([
            {'tgl': r.tanggal, 'jml': r.jumlah_telur, 'rsk': r.jumlah_telur_rusak} 
            for r in records
        ])
        summary = df.groupby('tgl').agg({'jml': 'sum', 'rsk': 'sum'}).reset_index()

        series_prod = QLineSeries()
        series_prod.setName("Produksi")
        series_rsk = QLineSeries()
        series_rsk.setName("Rusak")

        for _, row in summary.iterrows():
            dt = datetime.combine(row['tgl'], datetime.min.time())
            timestamp = int(dt.timestamp() * 1000)
            series_prod.append(timestamp, row['jml'])
            series_rsk.append(timestamp, row['rsk'])

        chart = QChart()
        chart.addSeries(series_prod)
        chart.addSeries(series_rsk)
        chart.setTitle("Analisis Produksi vs Rusak")

        axis_x = QDateTimeAxis()
        axis_x.setFormat("dd MMM")
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series_prod.attachAxis(axis_x)
        series_rsk.attachAxis(axis_x)

        axis_y = QValueAxis()
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series_prod.attachAxis(axis_y)
        series_rsk.attachAxis(axis_y)

        series_prod.setPen(QPen(QColor(0, 120, 215), 3))
        series_rsk.setPen(QPen(QColor(220, 53, 69), 2))

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.chart_layout.addWidget(chart_view)
        
    def clicked_grafik(self):
        
        if hasattr(self, 'canvas') and self.canvas.isVisible():
            self.canvas.hide()
            self.eggwidget.show()
            self.eggwidget.setText("Lihat Grafik")
        else:
            self.eggwidget.hide()
            self.update_graph()
            self.eggwidget.show()
            self.grafik_button.setText("Lihat Tabel")