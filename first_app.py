import streamlit as st
import numpy as np
import pandas as pd

#asdasd
#df1= pd.read_csv('C:/Users/jklue/OneDrive/Desktop/output_data4.csv')
#df = df1[["longitude","latitude"]]
#df = df.to_numpy()
#df = 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/3d-heatmap/heatmap-data.csv'
df = "https://raw.githubusercontent.com/trmer100/15min_cities/main/output_data55.csv"
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
            #"Hospitals": pdk.Layer(
            #    "HexagonLayer",
            #    data=df,
            #    get_position=["longitude", "latitude","hospital"],
            #    radius=200,
            #    elevation_scale=4,
            #    elevation_range=[0, 1000],
            #    extruded=True,
            #),
            "Schools": pdk.Layer(
                "ScatterplotLayer",
                data=df,
                get_position=["longitude", "latitude"],
                get_color=[200, 30, 0, 160],
                get_radius=1000,
                radius_scale=0.05,
            ),
            "Hospitals": pdk.Layer(
                "ScatterplotLayer",
                data=df,
                get_position=["longitude", "latitude"],
                get_color=[100, 20, 0, 160],
                get_radius=1000,
                radius_scale=0.05,
            ),
            #"Bart Stop Names": pdk.Layer(
            #    "icon-layer"
            #    data = df,
            #    get_position = ["longitude", "latitude"],
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

ssss
