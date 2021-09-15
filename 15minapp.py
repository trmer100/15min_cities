import streamlit as st
import pydeck as pdk
from geopy.geocoders import Nominatim
import pandas as pd
import numpy as np

# Creates a grid. Grid points consist out of longitude and latitude information. Distance between grid points = d. Amenities within a radius (r) of each grid point are assigned to each grid point and saved in a dictionary.
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

#Lat1 = 51.1238
#Lat2 = 51.3539
#Long1 = 6.6824
#Long2 = 6.94

#d = 0.001
#r = 0.01  # should be 1km

#connection to openstreetmaps_query.py read in of amenities_df.csv (cointains all amenities). 
#file_path = 'amenities_df.csv'
#cells = precompute_grid(file_path, Lat1, Lat2, Long1, Long2, d, r)
#cells_df = pd.DataFrame.from_dict(cells, orient = "index")
#pd.DataFrame.reset_index(cells_df, inplace = True)
#pd.DataFrame.rename(cells_df,columns={'level_0': 'latitude', 'level_1': 'longitude'}
#,inplace = True)
#cells_df.fillna(value = 0,inplace = True)
#cells_df.to_csv("cells_df.csv")


st.title("15-Minute-City")
st.write("Please insert your address and provide your preferences on the left. When finished, please click the """"Create Map""" "button to show how good your address and the surrounding area fits the 15-minute city approach!")
all_amenities_df = pd.read_csv("amenities_df.csv") 


individual_values = all_amenities_df[
    "amenity"].unique()  
amenities = []  
layer = [] 
slider_values = []


for x in individual_values:
    checkbox = st.sidebar.checkbox(x, True)
    slider_text = "Please choose your weight for " + x
    slider_value = st.sidebar.slider(slider_text, min_value=1, max_value=10, step=1)
    if checkbox == True:
        amenities.append(x)  # append x so the system knows which amenities to display on the map
        slider_values.append(slider_value)


def map(amenities):
    heat_layer = pdk.Layer(  # https://deck.gl/docs/api-reference/aggregation-layers/heatmap-layer
        "HeatmapLayer",
        cells_df,
        radiusPixels=125,
        opacity=0.3,
        get_position=["longitude", "latitude"],
        threshold=0.1,
        get_weight="total_score",
        pickable=True, )
    layer.append(heat_layer)

    for amenity_layer in amenities:
        amenity_layer = pdk.Layer(
            "ScatterplotLayer",
            data=all_amenities_df[all_amenities_df["amenity"] == amenity_layer],
            get_position=["longitude", "latitude"],
            get_color=[0, 0, 0, 1000],
            get_radius=200,
            radius_scale=0.05, )
        layer.append(amenity_layer)
    user_home = pdk.Layer(
        "ScatterplotLayer",
        data=df1[df1["amenity"] == "user_home"],
        get_position=["longitude", "latitude"],
        get_color=[185, 207, 234, 150],
        get_radius=600,
        radius_scale=1.05,)
    layer.append(user_home)

    st.pydeck_chart(pdk.Deck(map_style="mapbox://styles/mapbox/light-v9",
                             initial_view_state={"latitude": 51.24, "longitude": 6.85, "zoom": 11, "pitch": 50},
                             layers=layer))
    return


def address():
    geolocator = Nominatim(
        user_agent="my_user_agent")  # this and the line below will return the coordinates after providing an address in a certain format
    loc = geolocator.geocode(full_address)
    # st.write("latitude:" ,loc.latitude,"\nlongtitude:" ,loc.longitude)
    return pd.DataFrame({"amenity": ["user_home"], "latitude": [loc.latitude], "longitude": [loc.longitude]})


user_street = st.text_input("Street",
                            "Königsallee")  # st.text_input returns the input of the user to a variable, in this case user_street, "Königsallee" is the default value here
user_street_number = st.text_input("House number", "1")
user_city = st.text_input("City", "Düsseldorf")
user_country = "DE"
full_address = str(user_street) + " " + str(user_street_number) + "," + str(user_city) + "," + user_country

df1 = pd.DataFrame(address())  # assigning the address to df1 in order to use it in the function map()
user_address = address()

if st.button("Create Map"):
    cells_df = pd.read_csv("cells_df.csv")
    amenities_df = pd.DataFrame(amenities)
    slider_values_df = pd.DataFrame(slider_values)
    amenities_df.insert(1, "weight", slider_values_df, True)
    #amenities_df.to_csv("amenities_weights.csv")
    #user_address.to_csv("user_address.csv")
    cells_df["total_score"] = 0
    for amenity in individual_values:
        weight_df = amenities_df[amenities_df[0] == amenity]
        weight_raw = weight_df["weight"].values
        if weight_raw > 0:
            weight = weight_raw
        else:
            weight = 0
        weight = cells_df[amenity].astype(int) * weight
        cells_df["total_score"] = cells_df["total_score"] + weight
    map(amenities)


