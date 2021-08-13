import streamlit as st
import pydeck as pdk
from urllib.error import URLError
import pandas as pd


dfcsv= pd.read_csv('C:/Users/jklue/OneDrive/Desktop/output_data55.csv')

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

st.write("15-Minute-City-all in one dataframe")
map()


