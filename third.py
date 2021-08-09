
#is jupyter a must have?

import pandas as pd
import folium
import webbrowser

places= pd.read_excel('/Users/myb/MyDocuments/Techlabs/Fakedata.xlsx')


class Map:
    def __init__(self, center, zoom_start):
        self.center = center
        self.zoom_start = zoom_start

    def showMap(self):
        # Create map
        my_map = folium.Map(location=self.center, zoom_start=self.zoom_start)


        folium.Circle(
            radius=100,
            location=[51.233334, 6.783333],
            popup="big",
            color="crimson",
            fill=False,
        ).add_to(my_map)

        folium.Marker(
            location=[51.233334, 6.783333],
            popup="point",
            icon=folium.Icon(icon="cloud"),
        ).add_to(my_map)

        folium.CircleMarker(
            location=[51.233334, 6.783333],
            radius=50,
            popup="small",
            color="#3186cc",
            fill=True,
            fill_color="#3186cc",
        ).add_to(my_map)


        # Display map
        my_map.save("map.html")
        webbrowser.open("map.html")


# where to center our map
coords = [51.233334, 6.783333]
map = Map(center=coords, zoom_start=13)

map.showMap()