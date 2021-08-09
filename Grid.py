import numpy as np
from itertools import cycle

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

