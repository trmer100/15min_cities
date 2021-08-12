dfa = "https://raw.githubusercontent.com/trmer100/15min_cities/main/output_dfsoloa.csv"
dfb = "https://raw.githubusercontent.com/trmer100/15min_cities/main/output_dfsolob.csv"


def map():
    import streamlit as st
    import pandas as pd
    import pydeck as pdk

    from urllib.error import URLError

    try:
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
                data = dfa,
                get_position=["longitude", "latitude"],
                get_color=[200, 30, 0, 160],
                get_radius=1000,
                radius_scale=0.05,
            ),
            "Hospitals": pdk.Layer(
                "ScatterplotLayer",
                data=dfb,
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

map()
