import streamlit as st
import pydeck as pdk
from urllib.error import URLError
import pandas as pd
from geopy.geocoders import Nominatim


dfcsv= pd.read_csv('C:/Users/jklue/OneDrive/Desktop/output_data55.csv')  #import of local dataframe
def map():
    try:
        ALL_LAYERS = {
            "Hospital": pdk.Layer(
                "ScatterplotLayer",
                data=dfcsv[dfcsv["amenity"] == "school"],    #subsetting the dataframe to only use the specific amenity
                get_position=["longitude", "latitude"],  #pdk.layer needs the column names of the dataframe where the positions are written down
                get_color=[200, 30, 0, 160],
                get_radius=1000,
                radius_scale=0.05,
            ),
            "School": pdk.Layer(
                "ScatterplotLayer",
                data=dfcsv[dfcsv["amenity"] == "hospital"],
                get_position=["longitude", "latitude"],
                get_color=[100, 20, 0, 160],
                get_radius=1000,
                radius_scale=0.05,
            ),
            "Your address": pdk.Layer(
                "ScatterplotLayer",    #first approach to implement the location of the customer
                data=dfcsv[dfcsv["amenity"] == "user_home"],
                get_position = ["longitude", "latitude"],
                get_color = [100,20,0,160],
                get_radius = 1000,
                radius_scale = 1.05,
            ),
        }
        st.sidebar.markdown('### Map Layers')   # sidebar is used to show the tick boxes on the left side
        selected_layers = [
            layer for layer_name, layer in ALL_LAYERS.items()
            if st.sidebar.checkbox(layer_name, True)]
        if selected_layers:
            st.pydeck_chart(pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v9",    #this is the basic map
                initial_view_state={"latitude": 51.24,
                                    "longitude": 6.85, "zoom": 11, "pitch": 50},
                layers=selected_layers,
            ))
        else:
            st.pydeck_chart(pdk.Deck(  #this is used in case no box at all is ticked by the user, the map will still be there but no points are on it
                map_style="mapbox://styles/mapbox/light-v9",
                initial_view_state={"latitude": 51.24,
                                    "longitude": 6.85, "zoom": 11, "pitch": 50}))
    except URLError as e:
        st.error("""Connection error: %s""" % e.reason)

user_street = st.text_input("Street",  )  #st.text_input returns the input of the user to a variable, in this case user_street
user_street_number = st.text_input("House number", )
user_city = st.text_input("City",)
user_country ="DE"
full_address = str(user_street)+" "+str(user_street_number)+","+str(user_city)+","+user_country


def address():
    geolocator = Nominatim(user_agent="my_user_agent")   #this and the line below will return the coordinates after providing an address in a certain format
    loc = geolocator.geocode(full_address)
    st.write("latitude:" ,loc.latitude,"\nlongtitude:" ,loc.longitude)
    return pd.DataFrame({"amenity":["user_home"],"latitude":[loc.latitude],"longitude":[loc.longitude]})

st.write("15-Minute-City-all in one dataframe")
#st.button("Create Map")
if st.button("Run"):
    x = address()
    st.write(x)
    dfcsv = pd.concat([dfcsv, x])
    dfcsv.to_csv("dfappend.csv")

map()


#from grid2 import cells  # this will transfer the output from grid2 to this script
#dfcells = pd.DataFrame(cells)
#st.write(dfcells)

"""to do:
1. for loop
2. set base location of user
3. rearrange functions with button etc..
4. slider? for what should the slider be used?"""

#data of location is send to the team of markus</philip they will return the points of the grid
#take data of markus and philip and display these on a map with different color schemes

