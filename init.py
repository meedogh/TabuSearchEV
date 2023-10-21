import random
random.seed(13934803)

def randomize(x,y,f=0):
    if(f):
        return round(random.uniform(x,y),f)
    else:
        return random.randint(x,y)


grid_size = 50

car_num = 20
station_num = 30
charging_station_locations = [(random.randint(0, grid_size-1), random.randint(0, grid_size-1)) for _ in range(station_num)]
car_locations = charging_station_locations #[(random.randint(0, grid_size-1), random.randint(0, grid_size-1)) for _ in range(car_num)]

min_hours = 1
max_hours = 24

min_hours_length = 1
max_hours_length = 4

min_price_peak = 0.24
max_price_peak = 0.48

min_price_off_peak = 0.12
max_price_off_peak = 0.24

min_charging_rate = 0.12
max_charging_rate = 0.24

min_capacity = 24
max_capacity = 100

min_energy_consumption = 0.15
max_energy_consumption = 0.3

min_travel_price = 0.01
max_travel_price = 0.8

queue_length = 0 
serving_rate = 1
velocity = 80

max_iterations = 100
tabu_list_size = 100