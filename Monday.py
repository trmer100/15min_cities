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
    #print(cells) this gives you a dictionary with with long+lat as keys
    #print(cells.keys()) this gives just the grid
    return cells



def compute_score(grid_cells, weights):

    latitudes = [x[0] for x in list(grid_cells.keys())]
    longitudes = [x[1] for x in list(grid_cells.keys())]
    final_grid=[]
    for latitude in latitudes:
        target_lat = latitude
        row_longitude = []
        for longitude in longitudes:
            target_long = longitude
            np_cells = np.array([*grid_cells.keys()])
            target_coordinate = np.array((target_lat, target_long))
            distances = np.linalg.norm(np_cells - target_coordinate, axis=1)
            min_index = np.argmin(distances)
            target_cell = np_cells[min_index]
            amenities = grid_cells[(target_cell[0], target_cell[1])]
            cell_value = cells[tuple(target_cell)]


            score = 0
            for amenity in amenities:
                assert amenity in weights
                score += weights[amenity]*cell_value[amenity]
            row_longitude.append(score)
        final_grid.append(row_longitude)
    return final_grid


#weights
user_preferences = dict()
user_preferences["hospital"] = 2
user_preferences["school"] = 1
user_preferences["bar"] = 3
user_preferences["cafe"] = 5
user_preferences["fast_food"] = 2
user_preferences["college"] = 1
user_preferences["kindergarten"] = 1


#corner points of the grid
Lat1 = 51.1238
Lat2 = 51.3539
Long1 = 6.6824
Long2 = 6.94

d = 0.05  # current distance between the grid points
r = 0.01  # radius around the grid points (should be 1km)

file_path = 'dflong_output.csv' #source of amenities

#Function Nr.1
cells = precompute_grid(file_path, Lat1, Lat2, Long1, Long2, d, r)
print(cells)

#Function Nr.2
print(compute_score(cells, weights=user_preferences))


#cells_df = pd.DataFrame.from_dict(cells, orient = "index")
#cells_df.to_csv("precomputed_grid")
#pd.DataFrame.reset_index(cells_df, inplace = True)
#pd.DataFrame.rename(cells_df,columns={'level_0': 'latitude', 'level_1': 'longitude'} ,inplace = True)

