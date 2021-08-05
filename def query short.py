#run in python console to install overpy package: "pip install requests"

import overpy
import pandas as pd


def query(building_type):
    part1 = '[out:json][timeout:50];nwr(51.12129, 6.66877,51.36930, 6.96128)[amenity="'
    part2 = building_type
    part3 = '"];out center;'
    built_query = part1 + part2 + part3
    print(built_query)

    api = overpy.Overpass()  # overpy API
    result = api.query(built_query)  # API which is send to overpass
    list_of_node_tags = []  # initializing empty list for data_frame below
    for node in result.nodes:  # get tags information from each node
        node.tags['latitude'] = node.lat
        node.tags['longitude'] = node.lon
        node.tags['id'] = node.id
        list_of_node_tags.append(node.tags)
    for way in result.ways:  # get tags information from each node
        way.tags['id'] = way.id
        way.tags['latitude'] = way.center_lat
        way.tags['longitude'] = way.center_lon
        list_of_node_tags.append(way.tags)
    for relation in result.relations:  # get tags information from each node
        relation.tags['id'] = relation.id
        relation.tags['latitude'] = relation.center_lat
        relation.tags['longitude'] = relation.center_lon
        list_of_node_tags.append(relation.tags)
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

#amenities = ["hospital","fuel","biergarten"]
#for x in amenities:
#    data_prep(query(x))

final = data_prep(query("hospital"))

#final.to_excel("output_data3.xlsx")
#print(final.info())
#print(final)
#hospital, shop, biergarten .