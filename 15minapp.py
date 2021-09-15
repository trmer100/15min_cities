import streamlit as st
import pydeck as pdk
from geopy.geocoders import Nominatim
import pandas as pd
import numpy as np
import sys


def precompute_grid(csv_path, begin_lat, end_lat, begin_long, end_long, d, r):
    """
    Creates a grid. Grid points consist out of longitude and latitude information.
    Distance between grid points = d. Amenities within a radius (r) of each grid point are assigned to each grid point and saved in a dictionary.
    """
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


def map(amenities):
    heat_layer = pdk.Layer(
        "HeatmapLayer",
        cells_df,
        radiusPixels=125,
        opacity=0.3,
        get_position=["longitude", "latitude"],
        threshold=0.1,
        get_weight="total_score",
        pickable=True,
    )
    layer.append(heat_layer)

    for amenity_layer in amenities:
        amenity_layer = pdk.Layer(
            "ScatterplotLayer",
            data=all_amenities_df[all_amenities_df["amenity"] == amenity_layer],
            get_position=["longitude", "latitude"],
            get_color=[0, 0, 0, 1000],
            get_radius=200,
            radius_scale=0.05,
        )
        layer.append(amenity_layer)
    user_home = pdk.Layer(
        "ScatterplotLayer",
        data=user_address[user_address["amenity"] == "user_home"],
        get_position=["longitude", "latitude"],
        get_color=[185, 207, 234, 150],
        get_radius=600,
        radius_scale=1.05,
    )
    layer.append(user_home)

    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state={
                "latitude": 51.24,
                "longitude": 6.85,
                "zoom": 11,
                "pitch": 50,
            },
            layers=layer,
        )
    )
    return


def address():
    """this function translates the address of the user which is inserted in the 15minapp
    by the user into coordinates in order to display these on the map
    """
    geolocator = Nominatim(
        user_agent="my_user_agent"
    )
    loc = geolocator.geocode(full_address)
    return pd.DataFrame(
        {
            "amenity": ["user_home"],
            "latitude": [loc.latitude],
            "longitude": [loc.longitude],
        }
    )


if __name__ == "__main__":
    #this part below should only be used once per month in order to recreate the grid
    if len(sys.argv) > 1 and sys.argv[1] == "run_grid":
        Lat1 = 51.1238
        Lat2 = 51.3539
        Long1 = 6.6824
        Long2 = 6.94
        d = 0.001
        r = 0.01


        file_path = "amenities_df.csv"
        cells = precompute_grid(file_path, Lat1, Lat2, Long1, Long2, d, r)
        print("New Grid calculated")
        cells_df = pd.DataFrame.from_dict(cells, orient="index")
        pd.DataFrame.reset_index(cells_df, inplace=True)
        pd.DataFrame.rename(
            cells_df,
            columns={"level_0": "latitude", "level_1": "longitude"},
            inplace=True,
        )
        cells_df.fillna(value=0, inplace=True)
        cells_df.to_csv("cells_df.csv")

    st.title("15-Minute-City")
    st.write(
        "Please insert your address and provide your preferences on the left. When finished, please click the "
        """Create Map"""
        "button to show how good your address and the surrounding area fits the 15-minute city approach!"
    )
    all_amenities_df = pd.read_csv("amenities_df.csv")

    individual_values = all_amenities_df["amenity"].unique()
    amenities = []
    layer = []
    slider_values = []

    for individual_value in individual_values:
        checkbox = st.sidebar.checkbox(individual_value, True)
        slider_text = "Please choose your weight for " + individual_value
        slider_value = st.sidebar.slider(slider_text, min_value=1, max_value=10, step=1)
        if checkbox == True:
            amenities.append(individual_value)
            slider_values.append(slider_value)

    user_street = st.text_input(
        "Street", "Königsallee"
    )
    user_street_number = st.text_input("House number", "1")
    user_city = st.text_input("City", "Düsseldorf")
    user_country = "DE"
    full_address = (
        str(user_street)
        + " "
        + str(user_street_number)
        + ","
        + str(user_city)
        + ","
        + user_country
    )

    user_address = pd.DataFrame(
        address()
    )

    if st.button("Create Map"):
        cells_df = pd.read_csv("cells_df.csv")
        amenities_df = pd.DataFrame(amenities)
        slider_values_df = pd.DataFrame(slider_values)
        amenities_df.insert(1, "weight", slider_values_df, True)
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
        st.write(cells_df)
    # remove files. gitignore
