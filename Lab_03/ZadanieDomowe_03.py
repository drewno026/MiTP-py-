class Parking():
    def __init__(self, total_number_of_places):
        self.total_number_of_places = total_number_of_places
        self.free_places = self.total_number_of_places
        self.parking_revenue = 0
        self.plate_numbers_list = {
            "car": [],
            "truck": [],
            "two_wheeler": []
        }
        self.all_plates = {
            "car": [],
            "truck": [],
            "two_wheeler": []
        }

    def add_car(self, car):
        if self.free_places > 0:
            self.plate_numbers_list[car.car_type].append(car.plate_number)
            if car.plate_number not in self.all_plates[car.car_type]:
                self.all_plates[car.car_type].append(car.plate_number)
            self.free_places = self.free_places - 1
        else:
            print("Parking is full")
    def remove_car(self, car):
        if car.plate_number in self.plate_numbers_list[car.car_type]:
            self.plate_numbers_list[car.car_type].remove(car.plate_number)
            self.free_places += 1
            fee = self.calculate_fee(car.car_type)
            self.parking_revenue += fee
        else:
            print("Car is not on the parking")
    def calculate_fee(self, car_type):
        fees = {"car": 10, "truck": 30, "two_wheeler": 5}
        return fees.get(car_type, 0)
    def report(self):
        print("Number of free places: ", self.free_places)
        print("Currently parked cars", self.plate_numbers_list)
        print("Parking revenue: ", self.parking_revenue, "PLN")
        print("Currently parked vehicles: ")
        for car_type, plates in self.plate_numbers_list.items():
            print(f" - {car_type}: {plates}")
    def report_all_plates(self):
        print("List of all vehicles that used the parking lot:", self.all_plates)
    def report_truck_plates(self):
        print("List of trucks that used the parking lot: ", self.all_plates["truck"])
    def report_occupied_places(self):
        print("Number of occupied places: ", self.total_number_of_places - self.free_places)
    def report_revenue(self):
        print("Current revenue is equal: ", self.parking_revenue, "PLN")

class Car():
    parked = False
    def __init__(self, plate_number, color, car_type):
        self.plate_number = plate_number
        self.color = color
        self.car_type = car_type
    def park_in(self, parking):
        if self.parked == False:
            parking.add_car(self)
            self.parked = True
    def park_out(self, parking):
        if self.parked == True:
            parking.remove_car(self)
            self.parked = False
    def car_report(self):
        print("Plate number: ", self.plate_number)
        print("Color: ", self.color)
        print("Car type: ", self.car_type)

def test_parking():
    parking_w = Parking(5)
    car_1 = Car("KR123", "red", "car")
    car_2 = Car("KR321", "red", "car")
    car_3 = Car("KWA33", "blue", "truck")
    car_4 = Car("KWA44", "green", "truck")
    car_5 = Car("KR555", "black", "two_wheeler")
    car_6 = Car("KR66", "red", "two_wheeler")

    car_1.park_in(parking_w)
    car_2.park_in(parking_w)
    car_3.park_in(parking_w)
    car_2.park_out(parking_w)
    parking_w.report_occupied_places()      # 5
    car_2.park_in(parking_w)
    car_4.park_in(parking_w)
    car_5.park_in(parking_w)
    parking_w.report_occupied_places()
    parking_w.report_revenue()      # 9
    car_6.park_in(parking_w)
    car_1.park_out(parking_w)
    car_6.park_in(parking_w)
    parking_w.report_occupied_places()
    parking_w.report_revenue()      # 13

    car_2.park_out(parking_w)
    car_3.park_out(parking_w)
    car_4.park_out(parking_w)
    car_5.park_out(parking_w)
    car_6.park_out(parking_w)
    parking_w.report_occupied_places()
    parking_w.report_revenue()      # 15

    parking_w.report_all_plates()
    parking_w.report_truck_plates()

test_parking()