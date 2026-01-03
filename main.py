from data_loader import *
from pathlib import Path
import pickle

BASE_DIR = Path(__file__).resolve().parent

### Importing data
cities, airport_code, airport_lat, airport_lon, airport_runway_length = airportdata_loader() ## Index is city name
demand = demand_loader()  ## Index is (city_i, city_j)
hourly_demand = hourly_demand_calculator(demand, hour_coeff_loader())  ## Index is (city_i, city_j, hour)
aircraft_types, ac_speed, ac_seats, ac_TAT, ac_range, ac_runway_req, ac_daily_lease, ac_fixed_cost_per_flight, ac_cost_per_hour, ac_fuel_cost_param, fleet_availability = aircraft_fleet_loader() ## Index is aircraft type


## Precalculated distance dictionary loading
with open(BASE_DIR / "Estimated Data/distance_dict.pkl", "rb") as file:
    distance = pickle.load(file)

## Precalculated yield dictionary loading
with open(BASE_DIR / "Estimated Data/yield_dict.pkl", "rb") as file:
    yield_dict = pickle.load(file)  ## Index is (city_i, city_j)


### Costs
with open(BASE_DIR / "Estimated Data/time_based_costs.pkl", "rb") as file:
    time_based_costs = pickle.load(file) ## Index is (city_i, city_j, aircraft_type)

with open(BASE_DIR / "Estimated Data/fuel_based_costs.pkl", "rb") as file:
    fuel_based_costs = pickle.load(file) ## Index is (city_i, city_j, aircraft_type)

## Fixed costs are always the same so dont need to be calculated, index is aircraft_type

### Total cost per flight
with open(BASE_DIR / "Estimated Data/total_cost_per_flight_leg.pkl", "rb") as file:
    total_cost_per_flight_leg = pickle.load(file) ## Index is (city_i, city_j, aircraft_type)