
import streamlit as st

import pydeck
# 2014 location of car accidents in the UK
UK_ACCIDENTS_DATA = ('https://raw.githubusercontent.com/uber-common/'
                    'deck.gl-data/master/examples/3d-heatmap/heatmap-data.csv')
# Define a layer to display on a map
layer = pydeck.Layer(
    'HexagonLayer',
    UK_ACCIDENTS_DATA,
    get_position=['lng', 'lat'],
    auto_highlight=True,
    elevation_scale=50,
    pickable=True,
    elevation_range=[0, 3000],
    extruded=True,
    coverage=1)

aaa