from re import S
from database.db_session import sessionlocal
from database.entity.account import Account
class Passwordservice():
    def get_all(self):
        with sessionlocal() as session:
            return session.query(Account).all()
    def add_password(self, site, username, password):
        with sessionlocal() as session:
            acc = Account(site=site,username=username,password=password)
            session.add(acc)
            session.commit()
    def edit_password(self, id, site, username, password):
        with sessionlocal() as session:
            acc = session.query(Account).filter(Account.id == id).first()
            acc.site = site
            acc.username = username
            acc.password = password
            session.commit()
    def delete_password(self, id):
        with sessionlocal() as session:
            acc = session.query(Account).filter(Account.id == id).first()
            session.delete(acc)
            session.commit()
    def search_password(self, search):
        with sessionlocal() as session:
            return session.query(Account).filter(
                Account.site.like(f"%{search}%") |
                Account.username.like(f"%{search}%")
            ).all()