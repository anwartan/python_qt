from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QInputDialog
class password_manager_widget( QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("passwordmanager/passwordmanager.ui",self)
        self.add.clicked.connect(self.add_password)
    def add_password(self):
        site,ok=QInputDialog.getText(self,"Add acount","site:")
        if ok and site:
            username,ok=QInputDialog.getText(self,"Add acount","username:")
            if ok and username:
                password,ok=QInputDialog.getText(self,"Add acount","password:")
                if ok and password:
                    self.listWidget.addItem(f"{site} | {username} | {password}")
        else:
            return