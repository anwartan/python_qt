from database.db_session import sessionlocal
from database.entity.egg import Egg 
class Eggservice():   
    def getall(self):
        with sessionlocal() as session:
            return session.query(Egg).all()
    def add(self,tanggal,type,jumlah,rusak):
        with sessionlocal() as session:
            egg = Egg(tanggal=tanggal,type=type,jumlah=jumlah,rusak=rusak)
            session.add(egg)
            session.commit()
    def edit(self,id,tanggal,type,jumlah,rusak):
        with sessionlocal() as session:
            egg=session.get(Egg,id)
            if egg:
                egg.tanggal=tanggal
                egg.type=type
                egg.jumlah=jumlah
                egg.rusak=rusak
                session.commit()
    def delete(self, id):
        with sessionlocal() as session:
            egg=session.get(Egg,id) 
        if egg:
            session.delete(egg)
            session.commit()
    def import_eggs(self,filepath):
        pass
    def export(self):
        pass