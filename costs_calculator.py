from data_loader import *
from pathlib import Path
import pickle

BASE_DIR = Path(__file__).resolve().parent

cities, airport_code, airport_lat, airport_lon, airport_runway_length = airportdata_loader() ## Index is city name
aircraft_types, ac_speed, ac_seats, ac_TAT, ac_range, ac_runway_req, ac_daily_lease, ac_fixed_cost_per_flight, ac_cost_per_hour, ac_fuel_cost_param, fleet_availability = aircraft_fleet_loader() ## Index is aircraft type

## Precalculated distance dictionary loading
with open(BASE_DIR / "Estimated Data/distance_dict.pkl", "rb") as file:
    distance = pickle.load(file)

### Fixed costs are always the same so dont need to be calculated

### Time based costs
def time_based_costs_per_flight(aircraft_type, distance_ij):
    total_time_cost = ac_cost_per_hour[aircraft_type] * (distance_ij / ac_speed[aircraft_type])
    return total_time_cost

## Dictionary for all time based costs
time_based_costs = {}
for i in cities:
    for j in cities:
        for ac_type in aircraft_types:
            time_cost_ij = time_based_costs_per_flight(ac_type, distance[(i, j)])
            time_based_costs[(i, j, ac_type)] = time_cost_ij

## Save time based costs as pickle file
with open(BASE_DIR / "Estimated Data/time_based_costs.pkl", "wb") as file:
    pickle.dump(time_based_costs, file)

### Fuel based costs
def fuel_based_costs_per_flight(aircraft_type, distance_ij, f = 1.42):
    fuel_cost = ((ac_fuel_cost_param[aircraft_type] * f) / 1.5) * distance_ij
    return fuel_cost

## Dictionary for all fuel based costs
fuel_based_costs = {}
for i in cities:
    for j in cities:
        for ac_type in aircraft_types:
            fuel_cost_ij = fuel_based_costs_per_flight(ac_type, distance[(i, j)])
            fuel_based_costs[(i, j, ac_type)] = fuel_cost_ij

## Save fuel based costs as pickle file
with open(BASE_DIR / "Estimated Data/fuel_based_costs.pkl", "wb") as file:
    pickle.dump(fuel_based_costs, file)

### Total cost per flight
total_cost_per_flight_leg = {}
for i in cities:
    for j in cities:
        for ac_type in aircraft_types:
            total_cost = ac_fixed_cost_per_flight[ac_type] + time_based_costs[(i, j, ac_type)] + fuel_based_costs[(i, j, ac_type)]
            total_cost_per_flight_leg[(i, j, ac_type)] = total_cost

## Save total cost per flight leg as pickle file
with open(BASE_DIR / "Estimated Data/total_cost_per_flight_leg.pkl", "wb") as file:
    pickle.dump(total_cost_per_flight_leg, file)