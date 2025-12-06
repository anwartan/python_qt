from PyQt6.QtWidgets import QMainWindow, QInputDialog, QTableWidgetItem, QMessageBox, QFileDialog
from passwordmanager.service.accountservice import PasswordService
from PyQt6.uic import loadUi
import csv
from PyQt6.QtCore import Qt
class PasswordWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('passwordmanager/password.ui', self)
        self.add_button.clicked.connect(self.clicked_add)
        self.search_button.clicked.connect(self.search_site)
        self.deletedselected_button.clicked.connect(self.deleteselected)
        self.import_but.clicked.connect(self.importdata)
        self.export_but.clicked.connect(self.exportdata)
        self.pushButton.clicked.connect(self.toggle_show_password)
        self.edtrselected_button.clicked.connect(self.update)
        self.passwordservice = PasswordService()
        self.load_data()
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
        self.passwordservice.add(site,username,password)
        self.load_data()
    def load_data(self,query=None):
        if query:
            accounts=self.passwordservice.search(query)
        else:
            accounts = self.passwordservice.getall()
        self.tableWidget.setRowCount(len(accounts))
        for row, account in enumerate(accounts):
            item=QTableWidgetItem()
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            item.setText(str(account.id))
            item2=QTableWidgetItem()
            item2.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            item2.setText(str(account.site))
            item3=QTableWidgetItem()
            item3.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            item3.setText(str(account.username))
            item4=QTableWidgetItem()
            item4.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        
            item4.setText(str(account.password))
            self.tableWidget.setItem(row, 0, item)
            self.tableWidget.setItem(row, 1, item2)
            self.tableWidget.setItem(row, 2, item3)

            if self.showing_password:
                item4.setText(str(account.password))
                self.tableWidget.setItem(row, 3, item4)
            else:
                item4.setText(self.password(account.password))
                self.tableWidget.setItem(row, 3, item4)    
    def search_site(self):
        query=self.inputtext.text()
        self.load_data(query)
        #accounts=self.passwordservice.search(query)
        # self.tableWidget.setRowCount(len(accounts))
        # for account in accounts:
        #     row = accounts.index(account)
        #     self.tableWidget.setItem(row, 0, QTableWidgetItem(str(account.id)))
        #     self.tableWidget.setItem(row, 1, QTableWidgetItem(account.site))
        #     self.tableWidget.setItem(row, 2, QTableWidgetItem(account.username))
        #     self.tableWidget.setItem(row, 3, QTableWidgetItem(account.password))

    def deleteselected(self):
        selectedrow = self.tableWidget.currentRow()
        if selectedrow < 0:
            QMessageBox().warning(self, 'Warning', 'Please select a row to delete the data.')
            return
        print(selectedrow)
        accountid = int(self.tableWidget.item(selectedrow, 0).text())
        Question=QMessageBox.question(self, 'Confirmation', 'Do you want to save your changes?', 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                     QMessageBox.StandardButton.Yes)
        if Question == QMessageBox.StandardButton.No:
            return
        else:
            self.passwordservice.delete(accountid)
        self.load_data()
    def update(self):
        selectedrow = self.tableWidget.currentRow()
        if selectedrow < 0:
            QMessageBox().warning(self, 'Warning', 'Please select a row to edit the data.')
            return
        if not self.showing_password:
            # meminta master password
            input_pass, ok = QInputDialog.getText(
                self, "Master Password", "Enter master password:"
            )
            if not ok:
                return
            if input_pass != self.master_password:
                QMessageBox.warning(self, "Error", "Wrong master password!")
                return
            accountid = int(self.tableWidget.item(selectedrow, 0).text())
            site = self.tableWidget.item(selectedrow, 1).text()
            username = self.tableWidget.item(selectedrow, 2).text()
            password = self.tableWidget.item(selectedrow, 3).text()
            site, ok1 = QInputDialog.getText(self, 'Edit Account', 'site:',text=site)
            if ok1 == False:
                return
            username, ok2 = QInputDialog.getText(self, 'Edit username', 'username:',text=username)
            if ok2 == False:
                return
            password, ok3 = QInputDialog.getText(self, 'Edit password', 'password:',text=password)
            if ok3 == False:
                return
            self.passwordservice.edit(accountid,site,username,password)
        self.load_data()

    def importdata(self):
        filepath=QFileDialog.getSaveFileName(self,
            "Save File",
            "",
            "CSV Files (*.csv);;Text Files (*.txt);;All Files (*)"
        )
        importeddata=0
        with open("account.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader,None) 
            for row in reader:
                if len(row)<3:
                    continue
                site, username, password = row
                self.passwordservice.add(site, username, password)
                importeddata += 1
        self.load_data()
    def exportdata(self):
        filepath=QFileDialog.getSaveFileName(self,
            "Save File",
            "",
            "CSV Files (*.csv);;Text Files (*.txt);;All Files (*)"
        )
            
        accounts=self.passwordservice.getall()
        with open("account.csv", "w", newline="", encoding="utf-8") as file:
            writer= csv.writer(file)
            writer.writerow(["Site","Username","Password"])
            for account in accounts:
                writer.writerow([account.site,account.username,account.password])
            QMessageBox.information(self,'Export Successful','Data exported successfully!')
    def password(self,password):
        return "*" * len(password)
    def toggle_show_password(self):
        if not self.showing_password:
            # meminta master password
            input_pass, ok = QInputDialog.getText(
                self, "Master Password", "Enter master password:"
            )
            if not ok:
                return
            if input_pass != self.master_password:
                QMessageBox.warning(self, "Error", "Wrong master password!")
                return
            self.showing_password = True
            self.pushButton.setText("Hide Password")
        else:
            self.showing_password = False
            self.pushButton.setText("Show Password")
        self.load_data()
            


        
    master_password = "admin123"
    showing_password = False