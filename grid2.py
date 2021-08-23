
import pandas as pd
import numpy as np

# 51 is Latitude --> y movement
# 6  is Longitude --> x movement

#UL = (51.3539, 6.6824)
#UR = (51.3539, 6.94)
#LL = (51.1238, 6.6824)
#LR = (51.1238, 6.94)


Lat1= 51.1238
Lat2= 51.3539
Long1= 6.6824
Long2= 6.94

d = 0.05
r = 0.01 #should be 1km

Score = dict()
Score["hospital"] = 2
Score["school"] = 1

Latitude = np.arange(Lat1, Lat2, d)
Longitude = np.arange(Long1, Long2, d)

places= pd.read_csv('dfshort_output.csv')

places["latitude"] = places["latitude"].astype(float)
places["longitude"] = places["longitude"].astype(float)


def compute_value(Lat,Long,places):
    value= 0

    for index, row in places.iterrows():

        #print('index', index, 'row', row)
        if row['latitude'] >= Lat and row['latitude']<= Lat + r:
            if row['longitude'] >= Long and row['longitude'] <= Long + r:
                if row['amenity'] in Score:
                    value+= Score[row['amenity']] #which caluclation do we prefer?
                else:
                    print('could not find amenity '+row['amenity'])
    return value

cells = []
#cnt= 0
for Lat in Latitude:

    #print('Lat',Lat)

    for Long in Longitude:
        #print('Long', Long)
        #print('cnt', cnt, len(Latitude)*len(Longitude))
        #cnt = cnt + 1
        value = compute_value(Lat, Long, places)
        #print('value', value)
        cells.append([Lat, Long, value])

print(cells)





