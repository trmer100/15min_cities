import streamlit as st
import pydeck as pdk
from urllib.error import URLError
import pandas as pd
from geopy.geocoders import Nominatim





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

Lat1 = 51.1238
Lat2 = 51.3539
Long1 = 6.6824
Long2 = 6.94

d = 0.005
r = 0.01  # should be 1km

#file_path = 'dflong_output.csv'
#cells = precompute_grid(file_path, Lat1, Lat2, Long1, Long2, d, r)
#cells_df = pd.DataFrame.from_dict(cells, orient = "index")
#pd.DataFrame.reset_index(cells_df, inplace = True)
#pd.DataFrame.rename(cells_df,columns={'level_0': 'latitude', 'level_1': 'longitude'}
#,inplace = True)
#cells_df.fillna(value = 0,inplace = True)
#cells_df.to_csv("cells_df.csv")

#dfheat = pd.read_csv("Score_Data2.csv")
#st.write(dfheat)
#print(dfheat.dtypes)


st.write("15-Minute-City")
dfcsv = pd.read_csv("dflong_output.csv")  # import dataframe from github


individual_values = dfcsv[
    "amenity"].unique()  # individual values are taken from the dataframe, the result is a list of amenities
amenities2 = []  # empty dataframe for the loop below
layer = []  # empty layers for the different amenity layers
slider_values = []










for x in individual_values:
    checkbox = st.sidebar.checkbox(x, True)
    slider_text = "Please choose your weight for " + x
    slider_value = st.sidebar.slider(slider_text, min_value=1, max_value=10, step=1)
    if checkbox == True:
        amenities2.append(x)  # append x so the system knows which amenities to display on the map
        slider_values.append(slider_value)


def map(amenities):
    # just an example
    h = pdk.Layer(  # https://deck.gl/docs/api-reference/aggregation-layers/heatmap-layer
        "HeatmapLayer",
        cells_df,
        radiusPixels=50,
        opacity=0.9,
        get_position=["longitude", "latitude"],
        #aggregation=pdk.types.String("MEAN"),
        threshold=0.05,
        get_weight="total_score",
        pickable=True, )
    layer.append(h)

    for x in amenities2:
        x = pdk.Layer(
            "ScatterplotLayer",
            data=dfcsv[dfcsv["amenity"] == x],
            # subsetting the dataframe to only use the x amenity, it is repeated until all unique values of the dataframe column amenities are used
            get_position=["longitude", "latitude"],
            # pdk.layer needs the column names of the dataframe where the positions are written down
            get_color=[0, 0, 0, 1000],  # https://rgbacolorpicker.com/
            get_radius=200,
            radius_scale=0.05, )
        layer.append(x)
    p = pdk.Layer(  # we need an extra layer for displaying the users home
        "ScatterplotLayer",
        data=df1[df1["amenity"] == "user_home"],  # subsetting the dataframe to only use the specific amenity user_home
        get_position=["longitude", "latitude"],
        get_color=[185, 207, 234, 150],  # https://rgbacolorpicker.com/
        get_radius=1000,
        radius_scale=1.05, )
    layer.append(p)

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

def weights(amenity):
    bar1 = amenities2_df[amenities2_df[0]==amenity]
    bar2 = bar1["weight"].values
    if bar2 > 0:
        st.write("ticked")
        bar3 = bar2
    else:
        st.write("unticked")
        bar3 = 0
        weight = cells_df[amenity].astype(int)*bar3
    return weight














if st.button("Create Map"):
    cells_df = pd.read_csv("cells_df.csv")

    #cells_df.drop(columns="kindergarten", inplace=True)
    #cells_df.drop(columns="school", inplace=True)
    #cells_df.drop(columns="hospital", inplace=True)
    #st.write(cells_df)
    amenities2_df = pd.DataFrame(amenities2)
    slider_values_df = pd.DataFrame(slider_values)
    amenities2_df.insert(1, "weight", slider_values_df, True)
    amenities2_df.to_csv("amenities_weights.csv")
    user_address.to_csv("user_address.csv")
    #hospital
    hospital = amenities2_df[amenities2_df[0]=="hospital"]
    whospital = hospital["weight"].values
    whospital= cells_df["hospital"].astype(int)*(whospital+0)
    #bar
    bar1 = amenities2_df[amenities2_df[0]=="bar"]
    bar2 = bar1["weight"].values
    if bar2 > 0:
        st.write("ticked")
        bar3 = bar2
    else:
        st.write("unticked")
        bar3 = 0
    bar4 = cells_df["bar"].astype(int)*bar3
    #
    school1 = amenities2_df[amenities2_df[0] == "school"]
    school2 = school1["weight"].values
    if school2 > 0:
        st.write("ticked")
        school3 = school2
    else:
        st.write("unticked")
        school3 = 0
    school4 = cells_df["school"].astype(int) * school3

    cells_df["total_score"] = whospital + bar4 + school4
    st.write(cells_df)
    map(amenities2)
    st.write(weights("bar"))
st.write("hello")


#def weights(amenity):
#    bar1 = amenities2_df[amenities2_df[0]==amenity]
#    bar2 = bar1["weight"].values
#    if bar2 > 0:
#        st.write("ticked")
#        bar3 = bar2
#    else:
#        st.write("unticked")
#        bar3 = 0
#        bar4 = cells_df[amenity].astype(int)*bar3
#    return bar4

# st.write(user_address) #user output for makus and philipp
# st.write(amenities2)  #user output for markus and philipp
# st.write(slider_values) #user output for markus and philipp


# combining the tick box and the slider value


# st.write(amenities2_df)


# """to do:
# 1. rearrange functions with button etc..
# 2. slider? for what should the slider be used?
# 3. different colours for different amenities"""

# data of location is send to the team of markus</philip they will return the points of the grid
# take data of markus and philip and display these on a map with different color schemes

# this will transfer the output from grid2 to this script

# st.write(loc.latitude, loc.longitude)
# return (loc.latitude, loc.longitude)

# from grid2 import cells
# from scipy import spatial

# """
# listcells = list(cells.keys())
# tree = spatial.KDTree(listcells)
# x = tree.query([user_address])
# st.write(x)
# cells_index = (x[1])
# st.write(cells_index)
# i = cells_index.astype(int)
# print(i)
# print(listcells[i])"""