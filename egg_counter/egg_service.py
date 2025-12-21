from database.db_session import sessionlocal
from database.entity.counter import Counter
from database.entity.egg import Egg
class Eggservice():
    def get_all(self):
        with sessionlocal() as session:
            return session.query(Counter).all()
    def add_counter(self, py_date, tipe, jumlah_telur, jumlah_telur_rusak):
        with sessionlocal() as session:
            counter = Counter(tanggal=py_date, tipe=tipe, jumlah_telur=jumlah_telur, jumlah_telur_rusak=jumlah_telur_rusak)
            session.add(counter)
            session.commit()
    def edit_counter(self, id, tanggal, tipe, jumlah_telur, jumlah_telur_rusak):    
        with sessionlocal() as session:
            counter = session.query(Counter).filter(Counter.id == id).first()
            counter.tanggal = tanggal
            counter.tipe = tipe
            counter.jumlah_telur = jumlah_telur
            counter.jumlah_telur_rusak = jumlah_telur_rusak
            session.commit()
    def delete_counter(self, id):
        with sessionlocal() as session:
            counter = session.query(Counter).filter(Counter.id == id).first()
            session.delete(counter)
            session.commit()
    def get_graph_data(self):
        with sessionlocal () as session:
            data = session.query(Egg).order_by(Egg.tanggal).all()
            if not data: return [], []
            
            # Olah dengan Pandas untuk grouping
            df = pd.DataFrame([{
                'tanggal': e.tanggal, 
                'jumlah': e.jumlah
            } for e in data])
            
            summary = df.groupby('tanggal')['jumlah'].sum().reset_index()
            return summary['tanggal'].apply(lambda x: x.strftime('%Y-%m-%d'))
        