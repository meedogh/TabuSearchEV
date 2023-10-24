import matplotlib.pyplot as plt
from init import *
import calc

ev_parameters = []
cs_parameters = []

for i, cs_location in enumerate(charging_station_locations):
    cs_params = {
        'index': i,
        'location': cs_location,  
        'peak_hours': randomize(min_hours,max_hours),
        'peak_hours_length': randomize(min_hours,max_hours),
        'price_peak_hours': randomize(min_price_peak, max_price_peak, 2),
        'price_off_peak_hours': randomize(min_price_off_peak, max_price_off_peak, 2),
        'queue_length': queue_length,
        'serving_rate': serving_rate
    }
    cs_parameters.append(cs_params)

for i, ev_location in enumerate(car_locations):
    ev_params = {
        'index': i,
        'location': ev_location,
        'charging_rate': randomize(min_charging_rate, max_charging_rate, 2),    
        'current_charge': randomize(0.1, 1.0, 2),  
        'capacity': randomize(min_capacity, max_capacity),  
        'assigned_station': randomize(1, station_num),
        'energy_consumption': randomize(min_energy_consumption, max_energy_consumption, 2),
        'velocity': velocity,
        'travel_price': randomize(min_travel_price, max_travel_price, 2),
    }
    ev_parameters.append(ev_params)
# cs_parameters[29]['queue_length'] *= 0.1
# cs_parameters[28]['price_peak_hours'] *= 0.5
# cs_parameters[28]['price_off_peak_hours'] *= 0.5

for i, ev_params in enumerate(ev_parameters):
    print(f'EV {i+1} Parameters: {ev_params}')

for i, cs_params in enumerate(cs_parameters):
    print(f'Charging Station {i+1} Parameters: {cs_params}')


def objective_function_time(solution):
    total_time = 0

    for ev, cs in enumerate(solution):
        cs_params = cs_parameters[cs-1] 
        ev_params = ev_parameters[ev-1]

        d = calc.calculate_grid_distance(ev_params['location'], cs_params['location'])
        v = ev_params['velocity']
        Bfull = ev_params['capacity']
        Bv = ev_params['current_charge'] * ev_params['capacity']
        s = ev_params['charging_rate']
        q = cs_params['queue_length']
        l = cs_params['serving_rate']
        e = ev_params['energy_consumption']

        total_time += calc.Tserving(d,v,Bfull,Bv,s,q,l,e)
    return total_time


def objective_function_cost(solution):
    total_cost = 0

    for ev, cs in enumerate(solution):
        cs_params = cs_parameters[cs - 1] 
        ev_params = ev_parameters[ev - 1]

        d = calc.calculate_grid_distance(ev_params['location'], cs_params['location'])
        v = ev_params['velocity']
        Bfull = ev_params['capacity']
        Bv = ev_params['current_charge']
        q = cs_params['queue_length']
        l = cs_params['serving_rate']
        e = ev_params['energy_consumption']

        Ptravel = ev_params['travel_price']

        wait_time = calc.Twait(q,l)
        travel_time = calc.Ttravel(d, v)
        peak = (travel_time + wait_time) >= cs_params['peak_hours'] and (travel_time + wait_time) <= cs_params['peak_hours'] + cs_params['peak_hours_length']

        total_cost += calc.Cost(d, v, cs_params['price_peak_hours'], cs_params['price_off_peak_hours'], peak, Bfull, Bv, Ptravel, e)
    return total_cost

# def get_neighbors(solution):
#     neighbors = []
#     size = len(solution)
#     for i in range(size):
#         for j in range(station_num):
#             neighbor = solution[:]
#             neighbor[i] = j + 1
#             neighbors.append(neighbor)
#     return neighbors 


def get_neighbors(solution):
    neighbors = []
    size = len(solution)

    for _ in range(10):
        i = random.randint(0, size - 1)  
        j = random.randint(1, station_num)  
        neighbor = solution[:]  
        neighbor[i] = j  
        neighbors.append(neighbor)

    return neighbors

def tabu_search(initial_solution, max_iterations, tabu_list_size, objective_function):
    current_solution = initial_solution
    best_solution = current_solution
    tabu_list = []
    history = []
    best = []
    
    for _ in range(max_iterations):
        
        neighbors = get_neighbors(current_solution)
        best_neighbor = None
        best_neighbor_fitness = float('inf')

        for neighbor in neighbors:
            if neighbor not in tabu_list:
                neighbor_fitness = objective_function(neighbor)
                if neighbor_fitness < best_neighbor_fitness:
                    
                    best_neighbor_fitness = neighbor_fitness
                    best_neighbor = neighbor
                history.append(objective_function(neighbor))

        if best_neighbor is None:
            continue

        history.append(objective_function(current_solution))
        current_solution = best_neighbor
        tabu_list.append(current_solution) 

        if len(tabu_list) > tabu_list_size:
            tabu_list.pop(0) 


        if best_neighbor_fitness < objective_function(best_solution):
            best_solution = best_neighbor
        best.append(objective_function(best_solution))
    return best_solution, best, history



best_time, tabu_time, time_history = tabu_search([ev['assigned_station'] for ev in ev_parameters], max_iterations, tabu_list_size, objective_function_time)
best_cost, tabu_cost, cost_history = tabu_search([ev['assigned_station'] for ev in ev_parameters], max_iterations, tabu_list_size, objective_function_cost)


print(time_history)
print(cost_history)
print(best_time)
print(best_cost)


fig, axs = plt.subplots(2,3,layout="constrained")

def plot_map(ax, solution, title):
    ax.set_title(title)
    ax.set_xticks(range(grid_size))
    ax.set_yticks(range(grid_size))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(True)
    ax.tick_params(left = False, bottom = False) 

    for ev_idx, cs_idx in enumerate(solution):
        ev_params = ev_parameters[ev_idx - 1]
        cs_params = cs_parameters[cs_idx - 1] 
        d = calc.calculate_grid_distance(ev_params['location'], cs_params['location'])
        print("Distance between X and Y: {}".format(d))
        print("X: {}".format(ev_params['location']))
        print("Y: {}".format(cs_params['location']))
        station_color = (0, 0, min(cs_params['queue_length'] / 10, 1))
        ev_color = (min(ev_params['current_charge'], 1), 0, 0)
        ev_x, ev_y = ev_params['location']
        ax.scatter(ev_x, ev_y, c=[ev_color], s=20, marker='o', zorder = 15)
        cs_x, cs_y = cs_params['location']
        ax.scatter(cs_x, cs_y, c=[station_color], s=100, marker='*', zorder = 10)
        ax.arrow(ev_x, ev_y, cs_x - ev_x, cs_y - ev_y, color='green', head_width=0.4, head_length=0.4, zorder = 5)



plot_map(axs[0,0], best_time, "Best Time Solution")
print("------")
plot_map(axs[1,0], best_cost, "Best Cost Solution")



axs[0,1].plot(time_history, label = 'Time', color='orange')
axs[1,1].plot(cost_history, label = 'Cost')

axs[0,1].grid(ls=":")
axs[1,1].grid(ls=":")

axs[0,1].set_title("Time Optimization")
axs[1,1].set_title("Cost Optimization")

axs[0,1].legend()
axs[1,1].legend()

axs[0,2].plot(tabu_time, label = 'Time', color='orange')
axs[1,2].plot(tabu_cost, label = 'Cost')

axs[0,2].grid(ls=":")
axs[1,2].grid(ls=":")

axs[0,2].set_title("Time Optimization Tabu")
axs[1,2].set_title("Cost Optimization Tabu")

axs[0,2].legend()
axs[1,2].legend()

plt.savefig("test.jpg", dpi=400)
plt.show()
