import pandas as pd
import numpy as np


def precompute_grid(csv_path, begin_lat, end_lat, begin_long, end_long, d, r):
    places = pd.read_csv(csv_path)

    places["latitude"] = places["latitude"].astype(float)
    places["longitude"] = places["longitude"].astype(float)

    Latitude = np.arange(begin_lat, end_lat, d)
    Longitude = np.arange(begin_long, end_long, d)

    cells = dict()

    for _, row in places.iterrows():
        match_lat = False

        lat_place = row["latitude"]
        lon_place = row["longitude"]
        amenity = row["amenity"]

        for lat in Latitude:
            if match_lat is True and match_long is False:
                break

            match_long = False

            for long in Longitude:
                if lat <= lat_place <= lat + r:
                    if long <= lon_place <= long + r:
                        if (lat, long) not in cells:
                            cells[(lat, long)] = dict()
                        if amenity not in cells[(lat, long)]:
                            cells[(lat, long)][amenity] = 0

                        cells[(lat, long)][amenity] += 1

                        match_long = True
                        match_lat = True
                    elif match_long is True:
                        break
    return cells


def compute_score(grid_cells, target_lat, target_long, weights):
    np_cells = np.array([*grid_cells.keys()])
    target_coordinate = np.array((target_lat, target_long))
    distances = np.linalg.norm(np_cells - target_coordinate, axis=1)
    min_index = np.argmin(distances)
    target_cell = np_cells[min_index]
    #assert ((target_cell[0], target_cell[1]) in cells)
    amenities = grid_cells[(target_cell[0], target_cell[1])]

    score = 0
    for amenity in amenities:
        assert amenity in weights
        score += weights[amenity]

    return score


Lat1 = 51.1238
Lat2 = 51.3539
Long1 = 6.6824
Long2 = 6.94

d = 0.0005
r = 0.01  # should be 1km

file_path = 'dfshort_output.csv'

Score = dict()
Score["hospital"] = 2
Score["school"] = 1


cells = precompute_grid(file_path, Lat1, Lat2, Long1, Long2, d, r)

print(compute_score(cells, 51.14, 6.7, weights=Score))
