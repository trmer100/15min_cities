import pydeck as pdk
import streamlit as st
import pandas as pd

UK_ACCIDENTS_DATA = pd.read_csv("Score_Data2.csv")
st.write(UK_ACCIDENTS_DATA)
#layer = pdk.Layer(
    #'HexagonLayer',  # `type` positional argument is here
    #UK_ACCIDENTS_DATA,
    #get_position=["longitude", "latitude"],
    #auto_highlight=True,
    #elevation_scale=50,
    #pickable=True,
    #elevation_range=[0, 3000],
    #extruded=True,
    #coverage=1)

layer = pdk.Layer(
    "HeatmapLayer",
    UK_ACCIDENTS_DATA,
    opacity=0.9,
    get_position=["longitude", "latitude"],
    aggregation=pdk.types.String("MEAN"),
    threshold=1,
    get_weight="total_score",
    pickable=True,
)

st.pydeck_chart(pdk.Deck(map_style="mapbox://styles/mapbox/light-v9",
                             initial_view_state={"latitude": 51.24,"longitude": 6.85, "zoom": 11, "pitch": 50},
                             layers=layer))


