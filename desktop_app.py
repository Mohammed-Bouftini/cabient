from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt, QDateTime
import requests
import json

class DesktopApp(QMainWindow):
    def __init__(self):
        super().__init__()

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

        # Load data automatically when the application starts
        self.get_all_rendezvous_data()

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
                self.set_table_item(row_position, 4, item['fields']['date'])
                self.set_table_item(row_position, 5, item['fields']['time'])
                self.set_table_item(row_position, 6, item['fields']['presence'])

        else:
            self.table_widget.setRowCount(0)
            self.table_widget.setHorizontalHeaderLabels(["Error retrieving data"])

    def set_table_item(self, row, col, value):
        item = QTableWidgetItem(str(value))
        item.setFlags(item.flags() ^ Qt.ItemIsEditable)  # Make cells non-editable

        # Adjust the width of the Date and Time columns
        if col in {4, 5}:
            self.table_widget.setColumnWidth(col, 120)

        # Format Date and Time columns using QDateTime
        if col == 4:  # Date column
            date_time = QDateTime.fromString(value, "yyyy-MM-dd").toString("dd.MM.yyyy")
            item.setData(Qt.DisplayRole, date_time)

        if col == 5:  # Time column
            date_time = QDateTime.fromString(value, "HH:mm:ss").toString("hh:mm AP")
            item.setData(Qt.DisplayRole, date_time)

        self.table_widget.setItem(row, col, item)

if __name__ == "__main__":
    app = QApplication([])
    desktop_app = DesktopApp()
    desktop_app.show()
    app.exec_()
