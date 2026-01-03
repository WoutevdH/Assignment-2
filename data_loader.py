import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def airportdata_loader():
    filepath = BASE_DIR / "Data/DemandGroup2.xlsx"
    airport_data = pd.read_excel(
        filepath,
        skiprows=[0, 1, 2],
        usecols="B:V",
        nrows=5,
        index_col=0,
    )

    cities = list(airport_data)
    airport_code = airport_data.loc["ICAO Code"].to_dict()
    airport_lat = airport_data.loc["Latitude (deg)"].to_dict()
    airport_lon = airport_data.loc["Longitude (deg)"].to_dict()
    airport_runway_length = airport_data.loc["Runway (m)"].to_dict()
    return (
        cities,
        airport_code,
        airport_lat,
        airport_lon,
        airport_runway_length,
    )

cities, airport_code, airport_lat, airport_lon, airport_runway_length = airportdata_loader()


def demand_loader():
    filepath = BASE_DIR / "Data/DemandGroup2.xlsx"
    demand_data = pd.read_excel(
        filepath,
        skiprows=range(10),
        usecols="B:V",
        nrows=20,
        index_col=0,
    )

    (
        cities,
        airport_code,
        airport_lat,
        airport_lon,
        airport_runway_length,
    ) = airportdata_loader()

    icao_to_city = {code: city for city, code in airport_code.items()}

    demand_city_df = demand_data.rename(index=icao_to_city, columns=icao_to_city)

    demand = {
        (i, j): demand_city_df.loc[i, j] for i in cities for j in cities
    }


    return demand

def aircraft_fleet_loader():
    filepath = BASE_DIR / "Data/FleetType.xlsx"
    aircraft_data = pd.read_excel(
        filepath,
        index_col=0,
    )

    aircraft_types = aircraft_data.columns.tolist()

    ##Aircraft specs
    ac_speed = aircraft_data.loc["Speed [km/h]"].to_dict()
    ac_seats = aircraft_data.loc["Seats"].to_dict()
    ac_TAT = aircraft_data.loc["Average TAT [min]"].to_dict()
    ac_range = aircraft_data.loc["Maximum Range [km]"].to_dict()
    ac_runway_req = aircraft_data.loc["Runway Required [m]"].to_dict()

    ##Aircraft operating costs
    ac_daily_lease = aircraft_data.loc["Lease Cost [€/day]"].to_dict()
    ac_fixed_cost_per_flight = aircraft_data.loc["Fixed Operating Cost (Per Fligth Leg)  [€]"].to_dict()
    ac_cost_per_hour = aircraft_data.loc["Cost per Hour"].to_dict()
    ac_fuel_cost_param = aircraft_data.loc["Fuel Cost Parameter"].to_dict()

    ##Fleet availability
    fleet_availability = aircraft_data.loc["Fleet"].to_dict()

    return aircraft_types, ac_speed, ac_seats, ac_TAT, ac_range, ac_runway_req, ac_daily_lease, ac_fixed_cost_per_flight, ac_cost_per_hour, ac_fuel_cost_param, fleet_availability


def hour_coeff_loader():
    filepath = BASE_DIR / "Data/HourCoefficients.xlsx"
    hour_coeff_data = pd.read_excel(
        filepath,
        usecols='B,D:AA',
        skiprows=1,
        index_col=0,
    )

    ## Creates a dictionary which maps a city to its hourly coefficients
    hour_coeffs_per_city = {city: hour_coeff_data.loc[city].to_dict() for city in hour_coeff_data.index}

    return hour_coeffs_per_city

def hourly_demand_calculator(demand, hour_coeffs_per_city):
    hourly_demand = {}
    for i in cities:
        for j in cities:
            for hour in range(24):
                coeff_i = hour_coeffs_per_city[i][hour]
                hourly_demand[(i, j, hour)] = demand[(i, j)] * coeff_i

    return hourly_demand


