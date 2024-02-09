import math
import sys

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, second):
        return math.sqrt((second.x - self.x)**2 + (second.y - self.y)**2)

class Load:
    def __init__(self, load_id, pickup, dropoff):
        self.load_id = load_id
        self.pickup = pickup
        self.dropoff = dropoff

class Driver:
    def __init__(self):
        self.loads = []
        self.current_location = Point(0,0) # start at home
        self.total_distance = 0

def parse_loads(file_path):
    loads = []
    with open(file_path, 'r') as file:
        next(file)  # Skip the header line
        for line in file:
            load_id, pickup_str, dropoff_str = line.strip().split()
            pickup_x, pickup_y = map(float, pickup_str[1:-1].split(','))
            dropoff_x, dropoff_y = map(float, dropoff_str[1:-1].split(','))
            pickup = Point(pickup_x, pickup_y)
            dropoff = Point(dropoff_x, dropoff_y)
            loads.append(Load(int(load_id), pickup, dropoff))
    return loads

def assign_loads_to_drivers(loads):
    drivers = [Driver()]  # Start with one driver
    for load in loads:
        # Check if total_distance will be greater than 12 hour shift (including going home)
        if (drivers[-1].total_distance + drivers[-1].current_location.distance_to(load.pickup) + load.pickup.distance_to(load.dropoff) + load.dropoff.distance_to(Point(0,0))) <= 12 * 60: 
            drivers[-1].total_distance += drivers[-1].current_location.distance_to(load.pickup)
            drivers[-1].current_location = load.pickup

            drivers[-1].total_distance += drivers[-1].current_location.distance_to(load.dropoff)
            drivers[-1].current_location = load.dropoff

            drivers[-1].loads.append(load)
        else: 
            # if greater than 12 hour shift, then add a new driver
            new_driver = Driver()

            new_driver.total_distance += new_driver.current_location.distance_to(load.pickup)
            new_driver.current_location = load.pickup

            new_driver.total_distance += new_driver.current_location.distance_to(load.dropoff)
            new_driver.current_location = load.dropoff

            new_driver.loads.append(load)
            
            drivers.append(new_driver)
    return drivers

if __name__ == "__main__":
    input_file = sys.argv[1]
    loads = parse_loads(input_file)
    drivers = assign_loads_to_drivers(loads)

    # print final results
    for driver in drivers:
        print([load.load_id for load in driver.loads])
