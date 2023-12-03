from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidget, 
    QTableWidgetItem, QDialog, QLabel, QLineEdit, QPushButton, 
    QFormLayout, QMessageBox
)
from PySide6.QtCore import Qt, QDateTime
from PySide6.QtGui import QIcon
import requests
import json
from requests.auth import HTTPBasicAuth
import os

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        icon_path = os.path.join(os.path.dirname(__file__), 'static', 'images', 'favicon.ico')
        self.setWindowIcon(QIcon(icon_path))
        self.setWindowTitle("Login - Cabient Ouadie")
        self.setGeometry(200, 200, 300, 150)

        layout = QFormLayout(self)

        self.username_edit = QLineEdit(self)
        self.password_edit = QLineEdit(self)
        self.password_edit.setEchoMode(QLineEdit.Password)

        layout.addRow("Username:", self.username_edit)
        layout.addRow("Password:", self.password_edit)

        login_button = QPushButton("Login", self)
        login_button.clicked.connect(self.handle_login)
        layout.addRow(login_button)

    def handle_login(self):
        username = self.username_edit.text()
        password = self.password_edit.text()

        auth = HTTPBasicAuth(username, password)
        response = requests.get("http://localhost:8000/fr/api/admin_data_api/", auth=auth)

        if response.status_code == 200:
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")

class DesktopApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        
        self.setWindowTitle("Rendezvous App")
        self.setGeometry(200, 200, 900, 700)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Create a QTableWidget
        self.table_widget = QTableWidget(self)
        layout.addWidget(self.table_widget)

        # Set column headers
        headers = ["Nom", "Prenom", "Telephone", "Email", "Date", "Time", "Presence"]
        self.table_widget.setColumnCount(len(headers))
        self.table_widget.setHorizontalHeaderLabels(headers)
        self.search_edit = QLineEdit(self)
        self.search_edit.setPlaceholderText("Rechercher...")
        self.search_edit.textChanged.connect(self.update_table)
        layout.addWidget(self.search_edit)

        # Load data automatically when the application starts
        self.get_all_rendezvous_data()

    def get_all_rendezvous_data(self, search_term=None):
        url = "http://127.0.0.1:8000/fr/get_rendezvous_data/"
        response = requests.get(url)
        data = []
        if response.status_code == 200:
            data = json.loads(response.json().get('rendezvous_data', []))
            icon_path = os.path.join(os.path.dirname(__file__), 'static', 'images', 'favicon.ico')
            self.setWindowIcon(QIcon(icon_path))
            self.setWindowTitle(f"Cabient Ouadie")

            for item in data:
              if search_term is None or any(search_term.lower() in str(item['fields'][field]).lower() for field in ["nom", "prenom", "telephone", "email", "date", "time", "presence"]):
                row_position = self.table_widget.rowCount()
                self.table_widget.insertRow(row_position)
                for col, field in enumerate(["nom", "prenom", "telephone", "email", "date", "time", "presence"]):
                    self.set_table_item(row_position, col, item['fields'][field])
                
              email_column = ["nom", "prenom", "telephone", "email", "date", "time", "presence"].index("email")
              self.table_widget.setColumnWidth(email_column, 220)  

        else:
            print(f"Error retrieving data. Status code: {response.status_code}")
            print(f"Response content: {response.content.decode('utf-8')}")

            error_message = "Error retrieving data.\nPlease check your connection and try again."
            QMessageBox.critical(self, "Error", error_message)

            self.table_widget.setRowCount(0)
            self.table_widget.setHorizontalHeaderLabels(["Error retrieving data"])

    def set_table_item(self, row, col, value):
        item = QTableWidgetItem(str(value))
        item.setFlags(item.flags() ^ Qt.ItemIsEditable)

        if col in {4, 5}:
            self.table_widget.setColumnWidth(col, 120)

        if col == 4:
            date_time = QDateTime.fromString(value, "yyyy-MM-dd").toString("dd.MM.yyyy")
            item.setData(Qt.DisplayRole, date_time)

        if col == 5:
            date_time = QDateTime.fromString(value, "HH:mm:ss").toString("hh:mm AP")
            item.setData(Qt.DisplayRole, date_time)

        self.table_widget.setItem(row, col, item)
    
    def update_table(self):
      search_term = self.search_edit.text()
      self.get_all_rendezvous_data(search_term)


    def authenticate(self):
        login_dialog = LoginDialog()
        return login_dialog.exec_() == QDialog.Accepted

if __name__ == "__main__":
    app = QApplication([])

    login_dialog = LoginDialog()
    if login_dialog.exec_() == QDialog.Accepted:
        desktop_app = DesktopApp()
        desktop_app.show()
        app.exec_()
    else:
        QMessageBox.warning(None, "Authentication Failed", "You must login to access the application.")
