#run in python console to install overpy package: "pip install requests"

import overpy
import pandas as pd

#latitude = "51.2227"
#longitude = "6.7735"
#search_radius = "15000"
#building_type = "hospital"

def query(latitude, longitude, search_radius, building_type):
    part1 = '[out:json][timeout:50];(node["amenity"="'
    part2 = building_type
    part3 = '"](around:'
    part4 = '););out body;>;out skel qt;'
    q = search_radius + ',' + latitude + ',' + longitude  # (search_radius,latitude,longitude)
    built_query = part1 + part2 + part3 + q + part4  # arrange  to form query
    print(built_query)

    api = overpy.Overpass()  # overpy API
    result = api.query(built_query)  # API which is send to overpass
    list_of_node_tags = []  # initializing empty list for data_frame below
    for node in result.nodes:  # get tags information from each node
        node.tags['latitude'] = node.lat
        node.tags['longitude'] = node.lon
        node.tags['id'] = node.id
        list_of_node_tags.append(node.tags)
    data_frame = pd.DataFrame(list_of_node_tags)  # forming a pandas dataframe using list of dictionaries
    return data_frame


def data_prep(df):
    df.set_index("name",inplace=True)
    df_global_reduced= df[["latitude","longitude"]]
    df_global_reduced_float = df_global_reduced.copy()
    df_global_reduced_float["latitude"] = df_global_reduced_float["latitude"].astype("float")
    df_global_reduced_float["longitude"] = df_global_reduced_float["longitude"].astype("float")
    assert df_global_reduced_float["latitude"].dtype == "float"
    assert df_global_reduced_float["longitude"].dtype == "float"
    return df_global_reduced_float

df = data_prep(query("51.2227", "6.7735", "15000","biergarten"))
df.to_excel("output_data3.xlsx")
print(df.info())
print(df)
#abcdef#asdfasdf#asdf#a#sdf#as#df#asd#f#ad#f#asd#f#asd#f#asd#f