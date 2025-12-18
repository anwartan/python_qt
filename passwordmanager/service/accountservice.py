from database.db_session import sessionlocal
from database.entity.Account import Account 
class PasswordService():
    def getall(self):
        with sessionlocal() as session:
            return session.query(Account).all()
    def search(self,search):
        with sessionlocal() as session:
            return session.query(Account).filter(
                Account.site.like(f'%{search}%') | 
                Account.username.like(f'%{search}%')
            ).all()
    def add(self,site,username,password):
        with sessionlocal() as session:
            acc = Account(site=site,username=username,password=password)
            session.add(acc)
            session.commit()
    def edit(self,account_id,site,username,password):
        with sessionlocal() as session:
            acc=session.get(Account,account_id)
            if acc:
                acc.site=site
                acc.username=username
                acc.password=password
                session.commit()
    def delete(self, account_id):
        with sessionlocal() as session:
            acc=session.get(Account,account_id) 
        if acc:
            session.delete(acc)
            session.commit()
    def import_accounts(self,filepath):
        pass
    def export(self):
        pass