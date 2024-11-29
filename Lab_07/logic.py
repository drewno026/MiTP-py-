from PyQt5.QtCore import QDateTime

class Car:
    def __init__(self, plate_number, color, car_type, engine_capacity):
        self.plate_number = plate_number
        self.color = color
        self.car_type = car_type
        self.engine_capacity = engine_capacity
        self.parked = False
        self.total_fee = 0
        self.history = []  # List of tuples: (start_time, end_time, fee)

    def park_in(self, parking):
        if not self.parked:
            success = parking.add_car(self)
            if success:
                self.parked = True
                self.start_time = QDateTime.currentDateTime()
        else:
            print(f"Car with this plate {self.plate_number} is already on the parking.")

    def park_out(self, parking):
        if self.parked:
            end_time = QDateTime.currentDateTime()
            duration = self.start_time.secsTo(end_time)
            fee = parking.calculate_fee(self.car_type, duration)
            self.total_fee += fee
            self.history.append((self.start_time, end_time, fee))
            parking.remove_car(self, fee, self)
            self.parked = False
        else:
            print(f"Car with this plate {self.plate_number} is not on the parking.")

class Parking:
    def __init__(self):
        self.total_number_of_places = 5
        self.occupied_spaces = 0
        self.income = 0
        self.cars = []
        self.global_history = []

    def add_car(self, car):
        if self.occupied_spaces < self.total_number_of_places:
            self.occupied_spaces += 1
            self.cars.append(car)
            return True
        else:
            print("Parking is full")
            return False

    def remove_car(self, car, fee, vehicle):
        if car in self.cars:
            self.cars.remove(car)
            self.occupied_spaces -= 1
            self.income += fee
            self.global_history.append(
                (vehicle.plate_number, car.start_time, QDateTime.currentDateTime(), fee)
            )

    def calculate_fee(self, car_type, duration):
        rate_per_hour = {
            "car": 10,
            "truck": 30,
            "two wheeler": 5
        }
        rate = rate_per_hour.get(car_type, 0)
        units = (duration + 9) // 10
        if units == 0: units = 1
        return rate * units
