import streamlit as st
import pydeck as pdk
import pandas as pd
from geopy.geocoders import Nominatim
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


def compute_score(grid_cells, target_lat, target_long, weights):


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
            #assert ((target_cell[0], target_cell[1]) in cells)
            amenities = grid_cells[(target_cell[0], target_cell[1])]
            #print(target_cell,"here")
            cell_value = cells[tuple(target_cell)]


            score = 0
            for amenity in amenities:
                assert amenity in weights
                score += weights[amenity]*cell_value[amenity]
            row_longitude.append(score)
        final_grid.append(row_longitude)
    return final_grid

Lat1 = 51.1238
Lat2 = 51.3539
Long1 = 6.6824
Long2 = 6.94

d = 0.0505
r = 0.01  # should be 1km

file_path = 'dfshort_output.csv'

user_preferences = dict()
user_preferences["hospital"] = 2
user_preferences["school"] = 1
user_preferences["kindergarten"] = 4


cells = precompute_grid(file_path, Lat1, Lat2, Long1, Long2, d, r)
cells_df = pd.DataFrame.from_dict(cells, orient = "index")
#cells_df.to_csv("precomputed_grid")
#print(cells)
pd.DataFrame.reset_index(cells)
st.write(cells_df)
print(compute_score(cells, 51.14, 6.7, weights=user_preferences))


#from Jantest import user_address
#print(user_address)
#from Jantest import amenities2_df
#print(amenities2_df)



































st.write("15-Minute-City")
dfcsv= pd.read_csv("dflong_output.csv")#import dataframe from github
dfheat = pd.read_csv("Score_Data2.csv")

individual_values = dfcsv["amenity"].unique() #individual values are taken from the dataframe, the result is a list of amenities
amenities2=[] #empty dataframe for the loop below
layer=[] #empty layers for the different amenity layers
slider_values =[]
for x in individual_values:
    checkbox = st.sidebar.checkbox(x, True)
    slider_text = "Please choose your weight for " + x
    slider_value = st.sidebar.slider(slider_text, min_value = 1, max_value=10, step = 1)
    if checkbox == True:
        amenities2.append(x) #append x so the system knows which amenities to display on the map
        slider_values.append(slider_value)


def map(amenities):
    #just an example
    h = pdk.Layer(#https://deck.gl/docs/api-reference/aggregation-layers/heatmap-layer
        "HeatmapLayer",
        dfheat,
        radiusPixels = 50,
        opacity=0.9,
        #get_position=["longitude", "latitude"],
        aggregation=pdk.types.String("MEAN"),
        threshold=0.05,
        get_weight="total_score",
        pickable=True,)
    layer.append(h)

    for x in amenities2:
        x = pdk.Layer(
            "ScatterplotLayer",
            data=dfcsv[dfcsv["amenity"] == x],    #subsetting the dataframe to only use the x amenity, it is repeated until all unique values of the dataframe column amenities are used
            get_position=["longitude", "latitude"],  #pdk.layer needs the column names of the dataframe where the positions are written down
            get_color=[0, 0, 0, 1000], #https://rgbacolorpicker.com/
            get_radius=200,
            radius_scale=0.05,)
        layer.append(x)
    p = pdk.Layer(  #we need an extra layer for displaying the users home
        "ScatterplotLayer",
        data=df1[df1["amenity"] == "user_home"],    #subsetting the dataframe to only use the specific amenity user_home
        get_position=["longitude", "latitude"],
        get_color=[185, 207, 234, 150], #https://rgbacolorpicker.com/
        get_radius=1000,
        radius_scale=1.05,)
    layer.append(p)

    st.pydeck_chart(pdk.Deck(map_style="mapbox://styles/mapbox/light-v9",
                             initial_view_state={"latitude": 51.24,"longitude": 6.85, "zoom": 11, "pitch": 50},
                             layers=layer))
    return

def address():
    geolocator = Nominatim(user_agent="my_user_agent")   #this and the line below will return the coordinates after providing an address in a certain format
    loc = geolocator.geocode(full_address)
    #st.write("latitude:" ,loc.latitude,"\nlongtitude:" ,loc.longitude)
    return pd.DataFrame({"amenity":["user_home"],"latitude":[loc.latitude],"longitude":[loc.longitude]})


user_street = st.text_input("Street", "Königsallee")  #st.text_input returns the input of the user to a variable, in this case user_street, "Königsallee" is the default value here
user_street_number = st.text_input("House number", "1")
user_city = st.text_input("City", "Düsseldorf")
user_country ="DE"
full_address = str(user_street)+" "+str(user_street_number)+","+str(user_city)+","+user_country


df1 = pd.DataFrame(address()) #assigning the address to df1 in order to use it in the function map()
user_address = address()
if st.button("Create Map"):
    map(amenities2)


#combining the tick box and the slider value
amenities2_df = pd.DataFrame(amenities2)
slider_values_df = pd.DataFrame(slider_values)
amenities2_df.insert(1,"weight", slider_values_df,True)
amenities2_df.to_csv("amenities_weights.csv")
user_address.to_csv("user_address.csv")
st.write(amenities2_df)
st.write(user_address)




