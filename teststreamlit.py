import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd


#df1= pd.read_csv('C:/Users/jklue/OneDrive/Desktop/output_data4.csv')
#df = df1[["longitude","latitude"]]
#df = df.to_numpy()
#df = 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/3d-heatmap/heatmap-data.csv'
df = "https://raw.githubusercontent.com/trmer100/15min_cities/main/output_data3.csv?token=AUYHNTXLPPAT5JPSLM5UMDTBCUMUE"
#df = pd.read_csv("https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/3d-heatmap/heatmap-data.csv")
#print(UK_ACCIDENTS_DATA)
print(df)
#print(df1)
#df = df1[["longitude","latitude"]]
#print(df)
#print(df)
#print(df[df.amenity.isin(["hospital"])])
#st.write(df)
#st.map(df[df.amenity.isin(["hospital"])])
#st.write(df[df.amenity.isin(["hospital"])])

#if st.checkbox("hospital"):
 #   st.map(df[df.amenity.isin(["hospital"])])


#if st.checkbox("fuel"):
 #   st.map(df[df.amenity.isin(["fuel"])])


def map(df):
    import streamlit as st
    import pandas as pd
    import pydeck as pdk

    from urllib.error import URLError

    try:
        st.write(df)
        ALL_LAYERS = {
            "Bike Rentals": pdk.Layer(
                "HexagonLayer",
                data=df,
                get_position=["longitude", "latitude"],
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                extruded=True,
            ),
            #"Bart Stop Exits": pdk.Layer(
            #    "ScatterplotLayer",
            #    df,
            #    get_position=["lmg", "lat"],
            #    get_color=[200, 30, 0, 160],
            #    auto_highlight = True,
            #),
            #"Bart Stop Names": pdk.Layer(
            #    "TextLayer",
            #    data=from_data_file("bart_stop_stats.json"),
            #    get_position=["lon", "lat"],
            #    get_text="name",
            #    get_color=[0, 0, 0, 200],
            #    get_size=15,
            #    get_alignment_baseline="'bottom'",
            #),
            #"Outbound Flow": pdk.Layer(
            #    "ArcLayer",
            #    data=from_data_file("bart_path_stats.json"),
            #    get_source_position=["lon", "lat"],
            #    get_target_position=["lon2", "lat2"],
            #    get_source_color=[200, 30, 0, 160],
            #    get_target_color=[200, 30, 0, 160],
            #    auto_highlight=True,
            #    width_scale=0.0001,
            #    get_width="outbound",
            #    width_min_pixels=3,
            #    width_max_pixels=30,
            #),
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
            st.error("Please choose at least one layer above.")
    except URLError as e:
        st.error("""
            **This demo requires internet access.**
            Connection error: %s
        """ % e.reason)

map(df)
