from PyQt5.QtCore import QDateTime

class Car:
    def __init__(self, plate_number, color, vehicle_type, engine_capacity):
        self.plate_number = plate_number
        self.color = color
        self.vehicle_type = vehicle_type
        self.engine_capacity = engine_capacity
        self.parked = False
        self.total_fee = 0  # Suma opłat dla tego pojazdu
        self.history = []  # List of tuples: [(start_time, end_time, fee), ...]

    def parking_entry(self, parking):
        if not self.parked:
            success = parking.add_car(self)
            if success:
                self.parked = True
                self.start_time = QDateTime.currentDateTime()
        else:
            print(f"Samochód {self.plate_number} jest już na parkingu.")

    def parking_leave(self, parking):
        if self.parked:
            end_time = QDateTime.currentDateTime()
            duration = self.start_time.secsTo(end_time)
            fee = parking.calculate_fee(self.vehicle_type, duration)
            self.total_fee += fee
            self.history.append((self.start_time, end_time, fee))
            parking.remove_car(self, fee, self)
            self.parked = False
        else:
            print(f"Samochód {self.plate_number} nie jest na parkingu.")

class Parking:
    def __init__(self):
        self.total_number_of_spaces = 5
        self.occupied_spaces = 0
        self.income = 0
        self.cars = []  # List of parked cars
        self.global_history = []  # Historia całego parkingu

    def add_car(self, car):
        if self.occupied_spaces < self.total_number_of_spaces:
            self.occupied_spaces += 1
            self.cars.append(car)
            return True
        else:
            print("Parking jest pełny")
            return False

    def remove_car(self, car, fee, vehicle):
        if car in self.cars:
            self.cars.remove(car)
            self.occupied_spaces -= 1
            self.income += fee
            # Zapisujemy historię globalną
            self.global_history.append(
                (vehicle.plate_number, car.start_time, QDateTime.currentDateTime(), fee)
            )

    def calculate_fee(self, vehicle_type, duration):
        rate_per_hour = {
            "osobowy": 10,
            "ciężarowy": 30,
            "jednoślad": 5
        }
        rate = rate_per_hour.get(vehicle_type, 0)
        # Dzielimy czas na segmenty 10-sekundowe
        units = (duration + 9) // 10  # zaokrąglamy w górę
        if units == 0: units = 1
        return rate * units
