from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QLineEdit,
                             QComboBox, QTableWidget, QTableWidgetItem, QMessageBox, QTextEdit, QScrollArea)
from logic import Car, Parking
import sys


class ParkingGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Parking Manager")
        self.parking = Parking()
        self.cars = []
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Input fields
        input_layout = QHBoxLayout()

        self.plate_input = QLineEdit()
        self.plate_input.setPlaceholderText("Numer rejestracyjny")
        self.color_input = QLineEdit()
        self.color_input.setPlaceholderText("Kolor")

        self.type_input = QComboBox()
        self.type_input.addItems(["osobowy", "ciężarowy", "jednoślad"])

        self.capacity_input = QLineEdit()
        self.capacity_input.setPlaceholderText("Pojemność silnika")

        self.add_car_button = QPushButton("Dodaj samochód")
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
        self.table.setHorizontalHeaderLabels(["Rejestracja", "Kolor", "Typ", "Silnik", "Zaparkowany", "Opłaty"])
        self.table.cellClicked.connect(self.show_history_and_fees)

        main_layout.addWidget(self.table)

        # Vehicle details (initially hidden)
        self.vehicle_fee_label = QLabel("Całkowite opłaty pojazd: 0")
        self.vehicle_fee_label.hide()
        self.vehicle_history_label = QLabel("Historia parkowań:")
        self.vehicle_history_label.hide()

        main_layout.addWidget(self.vehicle_fee_label)
        main_layout.addWidget(self.vehicle_history_label)

        # Income label
        self.income_label = QLabel("Przychód: 0")
        main_layout.addWidget(self.income_label)

        # Global history
        self.global_history_label = QLabel("Historia parkingu:")
        self.global_history_text = QTextEdit()
        self.global_history_text.setReadOnly(True)

        self.global_history_area = QScrollArea()
        self.global_history_area.setWidget(self.global_history_text)
        self.global_history_area.setWidgetResizable(True)

        main_layout.addWidget(self.global_history_label)
        main_layout.addWidget(self.global_history_area)

        # Buttons
        button_layout = QHBoxLayout()
        self.enter_button = QPushButton("Wjazd")
        self.enter_button.clicked.connect(self.park_car)
        self.leave_button = QPushButton("Wyjazd")
        self.leave_button.clicked.connect(self.unpark_car)
        self.remove_button = QPushButton("Usuń pojazd")
        self.remove_button.clicked.connect(self.remove_car)

        button_layout.addWidget(self.enter_button)
        button_layout.addWidget(self.leave_button)
        button_layout.addWidget(self.remove_button)

        main_layout.addLayout(button_layout)

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
            QMessageBox.warning(self, "Błąd", "Wypełnij wszystkie pola!")
            return

        # Check for duplicate plate numbers
        if any(car.plate_number == plate for car in self.cars):
            QMessageBox.warning(self, "Błąd", f"Pojazd z numerem rejestracyjnym {plate} już istnieje!")
            return

        car = Car(plate, color, car_type, capacity)
        self.cars.append(car)
        self.update_table()

    def park_car(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Błąd", "Wybierz samochód!")
            return

        car = self.cars[row]
        car.park_in(self.parking)
        self.update_table()

    def unpark_car(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Błąd", "Wybierz samochód!")
            return

        car = self.cars[row]
        car.park_out(self.parking)
        self.update_table()
        self.income_label.setText(f"Przychód: {self.parking.income:.2f}")
        self.update_global_history()

    def remove_car(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Błąd", "Wybierz samochód!")
            return

        del self.cars[row]
        self.update_table()
        self.vehicle_fee_label.hide()
        self.vehicle_history_label.hide()

    def show_history_and_fees(self, row):
        car = self.cars[row]

        # Display total fees for the selected car
        self.vehicle_fee_label.setText(f"Całkowite opłaty: {car.total_fee:.2f}")
        self.vehicle_fee_label.show()

        # Display parking history for the selected car
        history = "\n".join([f"Od: {start.toString()} Do: {end.toString()} Opłata: {fee:.2f}"
                             for start, end, fee in car.history])
        if not history:
            history = "Brak historii parkowań pojazd."
        self.vehicle_history_label.setText(f"Historia parkowań pojazdu:\n{history}")
        self.vehicle_history_label.show()

    def update_table(self):
        self.table.setRowCount(len(self.cars))
        for i, car in enumerate(self.cars):
            self.table.setItem(i, 0, QTableWidgetItem(car.plate_number))
            self.table.setItem(i, 1, QTableWidgetItem(car.color))
            self.table.setItem(i, 2, QTableWidgetItem(car.car_type))
            self.table.setItem(i, 3, QTableWidgetItem(car.engine_capacity))
            self.table.setItem(i, 4, QTableWidgetItem("Tak" if car.parked else "Nie"))
            self.table.setItem(i, 5, QTableWidgetItem(f"{car.total_fee:.2f}"))

    def update_global_history(self):
        history = "\n".join([f"Rejestracja: {plate}, Od: {start.toString()} Do: {end.toString()}, Opłata: {fee:.2f}"
                             for plate, start, end, fee in self.parking.global_history])
        self.global_history_text.setText(history)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ParkingGUI()
    window.show()
    sys.exit(app.exec_())
