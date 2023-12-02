from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QLabel
from PySide6.QtCore import Qt  # Import the Qt module
import requests
import json

class DesktopApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.get_data_button = QPushButton("Get All RendezVous Data from Django", self)
        self.get_data_button.clicked.connect(self.get_all_rendezvous_data)
        layout.addWidget(self.get_data_button)

        # Create a QTableWidget
        self.table_widget = QTableWidget(self)
        layout.addWidget(self.table_widget)

        # Set column headers
        headers = ["Nom", "Prenom", "Telephone", "Email", "Date", "Time", "Presence"]
        self.table_widget.setColumnCount(len(headers))
        self.table_widget.setHorizontalHeaderLabels(headers)

    def get_all_rendezvous_data(self):
        url = "http://localhost:8000/get_rendezvous_data/"
        response = requests.get(url)

        if response.status_code == 200:
            data = json.loads(response.json().get('rendezvous_data', []))

            # Clear existing data in the table
            self.table_widget.setRowCount(0)

            # Populate the table with data
            for item in data:
                row_position = self.table_widget.rowCount()
                self.table_widget.insertRow(row_position)

                # Set data in the table
                self.set_table_item(row_position, 0, item['fields']['nom'])
                self.set_table_item(row_position, 1, item['fields']['prenom'])
                self.set_table_item(row_position, 2, item['fields']['telephone'])
                self.set_table_item(row_position, 3, item['fields']['email'])
                self.set_table_item(row_position, 4, str(item['fields']['date']))
                self.set_table_item(row_position, 5, str(item['fields']['time']))
                self.set_table_item(row_position, 6, str(item['fields']['presence']))

        else:
            self.table_widget.setRowCount(0)
            self.table_widget.setHorizontalHeaderLabels(["Error retrieving data"])

    def set_table_item(self, row, col, value):
        item = QTableWidgetItem(str(value))
        item.setFlags(item.flags() ^ Qt.ItemIsEditable)  # Make cells non-editable
        self.table_widget.setItem(row, col, item)

if __name__ == "__main__":
    app = QApplication([])
    desktop_app = DesktopApp()
    desktop_app.show()
    app.exec_()
