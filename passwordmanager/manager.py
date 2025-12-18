from fileinput import filename
from os import path
from re import A
import re
from PyQt6.QtWidgets import QMainWindow, QInputDialog, QTableWidgetItem, QMessageBox, QFileDialog
from PyQt6.uic import loadUi                
from numpy import delete
from sympy import Q
from database.entity import account
from passwordmanager.passwordservice.passwordservice import Passwordservice
import csv
class PasswordWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('passwordmanager/password.ui', self)
        self.add_button.clicked.connect(self.clicked_add)
        self.search_button.clicked.connect(self.clicked_search)
        self.delete_button.clicked.connect(self.clicked_delete)
        self.edit_button.clicked.connect(self.clicked_edit)
        self.import_button.clicked.connect(self.clicked_import)
        self.export_button.clicked.connect(self.clicked_export)
        self.accountservice = Passwordservice()
        self.clicked_search()
     
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
        self.accountservice.add_password(site, username, password)
        self.clicked_add()
    def clicked_search(self):
        query = self.inputtext.text() 
        accounts = self.accountservice.search_password(query)   
        self.tableWidget.setRowCount(len(accounts))
        for i in range(len(accounts)):
            row = i
            account = accounts[i]
            self.tableWidget.setItem(row, 0, QTableWidgetItem(str(account.id)))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(account.site))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(account.username))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(account.password))
        accounts = self.accountservice.get_all()
    def clicked_delete(self):
        comment = QMessageBox.question(self, 'Delete Account', 'Are you sure you want to delete this account?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        current_row = self.tableWidget.currentRow()
        id = int(self.tableWidget.item(current_row, 0).text())
        if comment == QMessageBox.StandardButton.Yes:
            self.accountservice.delete_password(id)
        else:
            print("no")
        self.clicked_search()
    def clicked_edit(self):
        current_row = self.tableWidget.currentRow()
        account_id = int(self.tableWidget.item(current_row, 0).text())
        site, ok1 = QInputDialog.getText(self, 'Add Account', 'site:')
        if ok1 == False:
            return
        username, ok2 = QInputDialog.getText(self, 'Add username', 'username:')
        if ok2 == False:
            return
        password, ok3 = QInputDialog.getText(self, 'Add password', 'password:')
        if ok3 == False:
            return
        self.accountservice.edit_password(account_id, site, username, password)
        self.clicked_search()
    def clicked_import(self):
        filename = QFileDialog.getOpenFileName(self,
        "import Accounts", "", "All Files(*);;Text Files(*.txt)")
        if not path:
            return
        with open(path, "r", encoding= "utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                if len(row) < 3:
                    continue
                site, username, password = row
                self.accountservice.add_password(site, username, password)
                imported_account += 1
        QMessageBox.information(self, "Import Successful", "Accounts imported successfully!")
        self.clicked_search()
    def clicked_export(self):
        fileName, _ = QFileDialog.getSaveFileName(self,
        "Save File", "account.csv", "All Files(*);;Text Files(*.txt)")
        accounts = self.accountservice.get_all()
        with open(fileName, 'w',newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(['Site', 'Username', 'Password'])
            for account in accounts:
                file.write(f"{account.id},{account.site},{account.username},{account.password}\n")
        QMessageBox.information(self, "Export Successful", "Accounts exported successfully!")
    # def load_data(self):
        # accounts = self.accountservice.get_all()
        # self.tableWidget.setRowCount(len(accounts))
        # for i in range(len(accounts)):
        #     row = i
        #     account = accounts[i]
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
