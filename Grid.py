import numpy as np
from itertools import cycle
import pandas as pd

TESTDATA = pd.read_csv('https://raw.githubusercontent.com/trmer100/15min_cities/main/dfshort_output.csv')

# four post comm.--> 10m
UL = ('51.3538', '6.6824')
UR = ('51.3538', '6.9398')
LL = ('51.1238', '6.6824')
LR = ('51.1238', '6.9398')

# selected bigger range--> all coordinates are included...
Lat = np.arange(51.1238, 51.3539, 0.0005)
Long = np.arange(6.6824, 6.94, 0.0005)

print(Lat.shape)
print(Long.shape)

# is it a list?
check_list = isinstance(Lat, list)
print(check_list)

LLat = list(Lat)
LLong = list(Long)

check_list2 = isinstance(LLat, list)
print(check_list2)

#This should be a list which starts with LL and ends with UR
grid = zip(cycle(LLong), LLat)

Tgrid = (list(grid))

print(Tgrid)

#our 15 minutes coordinate distance
# 51.22960797590307, 6.847133713714345
#51.235690529815805, 6.857753588940877

#changes start here

#transform list into df
Dgrid = pd.DataFrame(Tgrid)

# just for repetition and learning print(Dgrid.iloc[[0,1],[1]])

#read in amenities
places= pd.read_csv('dfshort_output.csv')

#check if places is a df
print(isinstance(places, pd.DataFrame))

#round places 4digits
Rplaces=places.round({'latitude': 4, 'longitude': 4})
print(Rplaces.head())

#current df are Rplaces and Dgrid

# rearange Dgrid
cols = Dgrid.columns.tolist()
cols = cols[-1:] + cols[:-1]
DgridO = Dgrid[cols]
print(DgridO)

# rename columns
DgridO.rename(columns={0: "longitudeG", 1: "latitudeG"},inplace = True)
print(DgridO)

# current df are Rplaces and DgridO

# doesnt't work ValueError: XA and XB must have the same number of columns (i.e. feature dimension.)
#from scipy.spatial.distance import cdist
#ary = cdist(Rplaces.iloc[:,1:], DgridO.iloc[:,1:], metric='euclidean')
#pd.DataFrame(ary)
#print(ary.head())

#my questions. What is the better option?
# Should value in the cell be a tuple?
#should we calculate with lists --> do we need to create a dictionaries? with Key values or sth like that?
# iterrow needs too much capacity? too much time?
# should we use haversine_distances?


#for i, row in DgridO.iterrows():