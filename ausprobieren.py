import pandas as pd

from grid2 import cells  # this will transfer the output from grid2 to this script
dfcells = pd.DataFrame(cells)

print(dfcells)

shortest_distance = None
shortest_distance_coordinates = None

point = (51.2290062, 6.8212808624507195)

for beispiel in cells:
    distance = compute_distance(point, beispiel)
    if distance < shortest_distance or shortest_distance is None:
        shortest_distance = distance
        shortest_distance_coordinates = beispiel
print(shortest_distance_coordinates)