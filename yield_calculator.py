import pickle
from pathlib import Path
from data_loader import airportdata_loader

BASE_DIR = Path(__file__).resolve().parent

##Import distances
with open(BASE_DIR / "Estimated Data/distance_dict.pkl", "rb") as file:
    distances = pickle.load(file)

cities, airport_code, airport_lat, airport_lon, airport_runway_length = airportdata_loader()

def calculate_yield(distance_ij):
    yield_ij = (5.9 * distance_ij ** (-0.76)) + 0.043
    return yield_ij


def calculate_all_yields(cities, distances) -> dict:
    yield_dict = {}
    for i in cities:
        for j in cities:
            if i == j:
                yield_dict[(i, j)] = 0
            else:
                yield_dict[(i, j)] = calculate_yield(distances[(i, j)])

    return yield_dict

yield_dict = calculate_all_yields(cities, distances)

## Save yield as pickle file
with open(BASE_DIR / "Estimated Data/yield_dict.pkl", "wb") as file:
    pickle.dump(yield_dict, file)