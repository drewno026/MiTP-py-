from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QLineEdit, QSizePolicy,
                             QComboBox, QTableWidget, QTableWidgetItem, QMessageBox, QTextEdit, QScrollArea)
from logic import Car, Parking
import sys

class ParkingGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Parking Manager")
        self.parking = Parking()
        self.cars = []
        self.setStyleSheet("background-color: lightblue;")
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Input fields
        input_layout = QHBoxLayout()

        self.plate_input = QLineEdit()
        self.plate_input.setPlaceholderText("Plate number")
        self.color_input = QLineEdit()
        self.color_input.setPlaceholderText("Color")

        self.type_input = QComboBox()
        self.type_input.addItems(["car", "truck", "two wheeler"])

        self.capacity_input = QLineEdit()
        self.capacity_input.setPlaceholderText("Engine capacity")
        self.capacity_input.setValidator(QIntValidator(0, 999999))

        self.add_car_button = QPushButton("Add car")
        self.add_car_button.clicked.connect(self.add_car)

        input_layout.addWidget(self.plate_input)
        input_layout.addWidget(self.color_input)
        input_layout.addWidget(self.type_input)
        input_layout.addWidget(self.capacity_input)
        input_layout.addWidget(self.add_car_button)

        main_layout.addLayout(input_layout)

        # Table of cars
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Plate number", "Color", "Type", "Engine capacity", "Parked", "Fees"])
        self.table.cellClicked.connect(self.show_history_and_fees)

        main_layout.addWidget(self.table)

        # Vehicle details
        self.vehicle_fee_label = QLabel("Total vehicle fees: 0")
        self.vehicle_fee_label.hide()
        self.vehicle_history_label = QLabel("Parking history:")
        self.vehicle_history_label.hide()

        main_layout.addWidget(self.vehicle_fee_label)
        main_layout.addWidget(self.vehicle_history_label)

        self.table.horizontalHeader().setStyleSheet("QHeaderView::section {background-color: lightblue; border: 1px solid black; }")
        self.table.setStyleSheet("QHeaderView::section { background-color: lightblue; color: black; }")

        # Buttons
        button_layout = QHBoxLayout()
        self.enter_button = QPushButton("Park in")
        self.enter_button.setStyleSheet("border: 1px solid black;")
        self.enter_button.clicked.connect(self.park_car)
        self.leave_button = QPushButton("Park out")
        self.leave_button.setStyleSheet("border: 1px solid black;")
        self.leave_button.clicked.connect(self.unpark_car)
        self.remove_button = QPushButton("Remove vehicle")
        self.remove_button.setStyleSheet("border: 1px solid black;")
        self.remove_button.clicked.connect(self.remove_car)

        button_layout.addWidget(self.enter_button)
        button_layout.addWidget(self.leave_button)
        button_layout.addWidget(self.remove_button)

        main_layout.addLayout(button_layout)

        # Income label
        self.income_label = QLabel("Income: 0")
        main_layout.addWidget(self.income_label)
        # Global history
        self.global_history_label = QLabel("Parking history:")
        self.global_history_text = QTextEdit()
        self.global_history_text.setReadOnly(True)

        self.global_history_area = QScrollArea()
        self.global_history_area.setWidget(self.global_history_text)
        self.global_history_area.setWidgetResizable(True)
        self.global_history_area.setFixedSize(600, 100)

        main_layout.addWidget(self.global_history_label)
        main_layout.addWidget(self.global_history_area)

        # Main widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def add_car(self):
        plate = self.plate_input.text()
        color = self.color_input.text()
        car_type = self.type_input.currentText()
        capacity = self.capacity_input.text()

        if not plate or not color or not capacity:
            QMessageBox.warning(self, "Error", "Please complete all fields")
            return

        if any(car.plate_number == plate for car in self.cars):
            QMessageBox.warning(self, "Error", f"Vehicle with this '{plate}' number plate already exists")
            return

        car = Car(plate, color, car_type, capacity)
        self.cars.append(car)
        self.update_table()

    def park_car(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Error", "Choose car")
            return

        car = self.cars[row]
        car.park_in(self.parking)
        self.update_table()

    def unpark_car(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Error", "Choose car")
            return

        car = self.cars[row]
        car.park_out(self.parking)
        self.update_table()
        self.income_label.setText(f"Income: {self.parking.income:.2f}")
        self.update_global_history()

    def remove_car(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Error", "Choose car")
            return

        del self.cars[row]
        self.update_table()
        self.vehicle_fee_label.hide()
        self.vehicle_history_label.hide()

    def show_history_and_fees(self, row):
        car = self.cars[row]

        self.vehicle_fee_label.setText(f"All fees: {car.total_fee:.2f}")
        self.vehicle_fee_label.show()

        history = "\n".join([f"From: {start.toString()} To: {end.toString()} Fee: {fee:.2f}"
                             for start, end, fee in car.history])
        if not history:
            history = "Parking history does not exists."
        self.vehicle_history_label.setText(f"Parking history:\n{history}")
        self.vehicle_history_label.show()

    def update_table(self):
        self.table.setRowCount(len(self.cars))
        for i, car in enumerate(self.cars):
            self.table.setItem(i, 0, QTableWidgetItem(car.plate_number))
            self.table.setItem(i, 1, QTableWidgetItem(car.color))
            self.table.setItem(i, 2, QTableWidgetItem(car.car_type))
            self.table.setItem(i, 3, QTableWidgetItem(car.engine_capacity))
            self.table.setItem(i, 4, QTableWidgetItem("Yes" if car.parked else "No"))
            self.table.setItem(i, 5, QTableWidgetItem(f"{car.total_fee:.2f}"))

    def update_global_history(self):
        history = "\n".join([f"Number plate: {plate}, From: {start.toString()} To: {end.toString()}, Fee: {fee:.2f}"
                             for plate, start, end, fee in self.parking.global_history])
        self.global_history_text.setText(history)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ParkingGUI()
    window.show()
    sys.exit(app.exec_())
