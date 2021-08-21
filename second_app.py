import streamlit as st
import pydeck as pdk
from urllib.error import URLError
import pandas as pd
from geopy.geocoders import Nominatim


dfcsv= pd.read_csv('C:/Users/jklue/OneDrive/Desktop/output_data55.csv')
##test
def map():
    try:
        ALL_LAYERS = {
            "Hospital": pdk.Layer(
                "ScatterplotLayer",
                data=dfcsv[dfcsv["amenity"] == "school"],
                get_position=["longitude", "latitude"],
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
        }
        st.sidebar.markdown('### Map Layers')
        selected_layers = [
            layer for layer_name, layer in ALL_LAYERS.items()
            if st.sidebar.checkbox(layer_name, True)]
        if selected_layers:
            st.pydeck_chart(pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v9",
                initial_view_state={"latitude": 51.24,
                                    "longitude": 6.85, "zoom": 11, "pitch": 50},
                layers=selected_layers,
            ))
        else:
            st.pydeck_chart(pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v9",
                initial_view_state={"latitude": 51.24,
                                    "longitude": 6.85, "zoom": 11, "pitch": 50}))
    except URLError as e:
        st.error("""Connection error: %s""" % e.reason)


def address():
    user_street = st.text_input("Street",  )
    user_street_number = st.text_input("House number", )
    user_city = st.text_input("City",)
    user_country ="DE"
    full_address = str(user_street)+" "+str(user_street_number)+","+str(user_city)+","+user_country
    geolocator = Nominatim(user_agent="my_user_agent")
    loc = geolocator.geocode(full_address)
    st.write("latitude:" ,loc.latitude,"\nlongtitude:" ,loc.longitude)

st.write("15-Minute-City-all in one dataframe")
address()
map()