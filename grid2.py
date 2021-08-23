
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

d = 0.0005
r = 0.01 #should be 1km

Score = dict()
Score["hospital"] = 2
Score["school"] = 1

Latitude = np.arange(Lat1, Lat2, d)
Longitude = np.arange(Long1, Long2, d)

places= pd.read_csv('dfshort_output.csv')

places["latitude"] = places["latitude"].astype(float)
places["longitude"] = places["longitude"].astype(float)


def compute_value(Lat,Long):
    value= 0
    for index, row in places.iterrows():
        if row['latitude'] >= Lat and row['latitude']<= Lat + r:
            if row['longitude'] >= Long and row['longitude'] <= Long + r:
                if row['amenity'] in Score:
                    value+= Score[row['amenity']]
                else:
                    print('could not find amenity '+row['amenity'])
    return value

cells = []
for Lat in Latitude:
    for Long in Longitude:
        value = compute_value(Lat, Long)
        cells.append([Lat, Long, value])


#visualization is a different topic (Jan)
# explanation of break points





#PlusLa= np.array([0,d])
#PlusLo= np.array([d,0])

#StartPoint= np.array([51.3538,6.6824])
# PlusLa--> UR
# PlusLo--> LL
#cells = []
#for lat in Lat:
    #for lon in Long:
    #cell_mid_lat = (Lat+d/2)
    #cell_mid_long = (Long+d/2)
    #value = call_function_that_creates_value_based_on_lat_lon(cell_mid_lat, cell_mid_long)
    #cells.append([cell_mid_lat, cell_mid_lon, value])






#ListHorizontalStart= []
#for i in OnlyLat:
   # ListHorizontalStart.extend([i+PlusLa])
#print(ListHorizontal)


#ListHorizontalStart= []
#for i in UL:
 #  ListHorizontalStart.extend([i+PlusLa])
  # if i == UR:
   #    break

#ListHorizontal1 = []
#while UL < UR :
    #for ListHorizontal1.extend(UL+PlusLa)






#IwantList= [y,x]




