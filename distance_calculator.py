import numpy as np
import pickle
from data_loader import airportdata_loader
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

cities, airport_code, airport_lat, airport_lon, airport_runway_length = airportdata_loader()

def calculate_distance(
    lat_i,
    lat_j,
    lon_i,
    lon_j,
    Re=6371,
) -> float:
    R = Re  # Radius of the Earth in kilometers
    lat_i_rad = np.radians(lat_i)
    lat_j_rad = np.radians(lat_j)
    delta_lat = np.radians(lat_j - lat_i)
    delta_lon = np.radians(lon_j - lon_i)

    a = (
        np.sin(delta_lat / 2) ** 2
        + np.cos(lat_i_rad) * np.cos(lat_j_rad) * np.sin(delta_lon / 2) ** 2
    )
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    distance = R * c
    return distance

def calculate_all_distances(cities, airport_lat, airport_lon) -> dict:
    distance_dict = {}
    for i in cities:
        for j in cities:
            distance_ij = calculate_distance(
                airport_lat[i], airport_lat[j], airport_lon[i], airport_lon[j]
            )
            distance_dict[(i, j)] = distance_ij

    return distance_dict

distance_dict = calculate_all_distances(
    cities, airport_lat, airport_lon)

with open(BASE_DIR / "Estimated Data/distance_dict.pkl", "wb") as file:
    pickle.dump(distance_dict, file)
