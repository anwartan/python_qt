from database.db_session import sessionlocal
from database.entity.egg import Egg
import csv
import datetime

class Eggservice():
    def get_all(self):
        with sessionlocal() as session:
            return session.query(Egg).all()

    # Compatibility alias used by GUI
    def getall(self):
        return self.get_all()

    def add(self, tanggal, type, jumlah, rusak):
        with sessionlocal() as session:
            egg = Egg(tanggal=tanggal, type=type, jumlah=jumlah, rusak=rusak)
            session.add(egg)
            session.commit()

    def edit(self, id, tanggal, type, jumlah, rusak):
        with sessionlocal() as session:
            egg = session.get(Egg, id)
            if egg:
                egg.tanggal = tanggal
                egg.type = type
                egg.jumlah = jumlah
                egg.rusak = rusak
                session.commit()

    def delete(self, id):
        with sessionlocal() as session:
            egg = session.get(Egg, id)
            if egg:
                session.delete(egg)
                session.commit()

    def import_eggs(self, filepath):
        imported = 0
        with sessionlocal() as session:
            with open(filepath, newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if len(row) < 4:
                        continue
                    t, tipe, j, r = row
                    try:
                        t = datetime.date.fromisoformat(t)
                    except Exception:
                        continue
                    egg = Egg(tanggal=t, type=tipe, jumlah=int(j), rusak=int(r))
                    session.add(egg)
                    imported += 1
            session.commit()
        return imported

    def export(self):
        # Return list of egg objects; caller can write to CSV if needed
        return self.get_all()