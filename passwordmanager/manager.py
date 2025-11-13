from PyQt6.QtWidgets import QMainWindow, QInputDialog
from PyQt6.uic import loadUi
class PasswordWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('passwordmanager/password.ui', self)
        self.add_button.clicked.connect(self.clicked_add)
    def clicked_add(self):
        site, ok1 = QInputDialog.getText(self, 'Add Account', 'site:')
        if ok1 == False:
            return
        username, ok2 = QInputDialog.getText(self, 'Add username', 'username:')
        if ok2 == False:
            return
        password, ok3 = QInputDialog.getText(self, 'Add password', 'password:')
        if ok3 == False:
            return
        print(site, ok1)
        print(username, ok2)
        print(password, ok3)