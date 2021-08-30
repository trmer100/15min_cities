import streamlit as st
import pydeck as pdk
from urllib.error import URLError
import pandas as pd
from geopy.geocoders import Nominatim

st.write("15-Minute-City")
dfcsv= pd.read_csv("output_data55.csv")  #import dataframe from github
def map():
    individual_values = dfcsv["amenity"].unique() #individual values are taken from the dataframe, the result is a list of amenities
    amenities2=[] #empty dataframe for the loop below
    layer=[] #empty layers for the different amenity layers

    for x in individual_values:
        checkbox = st.checkbox(x)
        if checkbox == True:
            amenities2.append(x) #append x so the system knows which amenities to display on the map

    for x in amenities2:
        x = pdk.Layer(
            "ScatterplotLayer",
            data=dfcsv[dfcsv["amenity"] == x],    #subsetting the dataframe to only use the x amenity, it is repeated until all unique values of the dataframe column amenities are used
            get_position=["longitude", "latitude"],  #pdk.layer needs the column names of the dataframe where the positions are written down
            get_color=[200, 30, 0, 160],
            get_radius=1000,
            radius_scale=0.05,)
        layer.append(x)
    #p = pdk.Layer(  #we need an extra layer for displaying the users home
    #    "ScatterplotLayer",
    #    data=df1[df1["amenity"] == "user_home"],    #subsetting the dataframe to only use the specific amenity user_home
    #    get_position=["longitude", "latitude"],
    #    get_color=[200, 30, 0, 160],
    #    get_radius=1000,
    #    radius_scale=1.05,)
    #layer.append(p)

    st.pydeck_chart(pdk.Deck(map_style="mapbox://styles/mapbox/light-v9",
                             initial_view_state={"latitude": 51.24,"longitude": 6.85, "zoom": 11, "pitch": 50},
                             layers=layer))


user_street = st.text_input("Street",  )  #st.text_input returns the input of the user to a variable, in this case user_street
user_street_number = st.text_input("House number", )
user_city = st.text_input("City",)
user_country ="DE"
full_address = str(user_street)+" "+str(user_street_number)+","+str(user_city)+","+user_country


def address():
    geolocator = Nominatim(user_agent="my_user_agent")   #this and the line below will return the coordinates after providing an address in a certain format
    loc = geolocator.geocode(full_address)
    st.write("latitude:" ,loc.latitude,"\nlongtitude:" ,loc.longitude)
    #st.write(loc.latitude,loc.longitude)
    #return pd.DataFrame({"amenity":["user_home"],"latitude":[loc.latitude],"longitude":[loc.longitude]})
    return (loc.latitude, loc.longitude)


#df1 = pd.DataFrame(address()) #assigning the address to df1 in order to use it in the function map()
user_address = address()
st.write(user_address)
map()


"""to do:
1. rearrange functions with button etc..
2. slider? for what should the slider be used?"""

#data of location is send to the team of markus</philip they will return the points of the grid
#take data of markus and philip and display these on a map with different color schemes

#st.write(dfcells[0] - df1["latitude"])

from grid2 import cells  # this will transfer the output from grid2 to this script
from scipy import spatial
listcells = list(cells.keys())
tree = spatial.KDTree(listcells)
x = tree.query([user_address])
cells_index = (x[1])

first_key = list(cells)[cells_index]
print(first_key)