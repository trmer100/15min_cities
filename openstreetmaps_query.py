# The openstreetmaps_query is used to gather data from openstreetmaps about amenities in a certain area. This is only used once per month.
import overpy
import pandas as pd
import time



def query(building_type="hospital"):
    """
    building_type: .....
    this function requests the data for one amenity only in a certain location,
    the output is one dataframe with the exact locations of a certain amenity
    return: ...#docstringsexampel
    """
    query_part1 = (
        '[out:json][timeout:50];nwr(51.1238, 6.6824,51.3538, 6.9398)[amenity="'
    )
    query_part2 = building_type
    query_part3 = '"];out center;'
    built_query = query_part1 + query_part2 + query_part3
    api = overpy.Overpass()
    result = api.query(built_query)
    list_of_node_tags = []
    for node in result.nodes:
        node.tags["latitude"] = node.lat
        node.tags["longitude"] = node.lon
        node.tags["id"] = node.id
        list_of_node_tags.append(node.tags)
    for way in result.ways:
        way.tags["id"] = way.id
        way.tags["latitude"] = way.center_lat
        way.tags["longitude"] = way.center_lon
        list_of_node_tags.append(way.tags)
    for relation in result.relations:
        relation.tags["id"] = relation.id
        relation.tags["latitude"] = relation.center_lat
        relation.tags["longitude"] = relation.center_lon
        list_of_node_tags.append(relation.tags)
    data_frame = pd.DataFrame(
        list_of_node_tags
    )
    return data_frame


# the returned data_frame from the query needs to be changed in order to use it
def data_prep(df):
    df_global_reduced = df[["name", "latitude", "longitude"]]
    df_global_reduced_float = df_global_reduced.copy()
    df_global_reduced_float["latitude"] = df_global_reduced_float["latitude"].astype(
        "float"
    )
    df_global_reduced_float["longitude"] = df_global_reduced_float["longitude"].astype(
        "float"
    )
    assert df_global_reduced_float["latitude"].dtype == "float"
    assert df_global_reduced_float["longitude"].dtype == "float"
    return df_global_reduced_float

if __name__ == "__main__":
    # this list can be changed by the user in order gather different amenity types or extend it, to
    # make it more complex, the source for these amenities are: ("https://wiki.openstreetmap.org/wiki/Key:amenity")
    amenities = [
        "hospital",
        "dentist",
        "pharmacy",
        #"school",
        #"kindergarten",
        #"library",
        #"university",
        #"bar",
        #"cafe",
        #"bicycle_repair_station",
        #"cinema",
        #"public_bppl",
    ]
    #change variables
    # the function "query" provides only one amenitiy on each request,
    # therefore we need a loop to repeat it for each amenity we are interested in
    df1 = pd.Series([""])
    for x in amenities:
        df2 = pd.Series([""])
        df2 = data_prep(query(building_type=x))
        df2["amenity"] = pd.Series([x for g in range(len(df2.index))])
        df1 = pd.concat([df1, df2])
        time.sleep(30)  # sleep timer to avoid "too many requests at the server"

    # creation of amenities_df, this dataframe is used in the 15minapp later
    amenities_df = df1[["amenity", "latitude", "longitude"]]
    amenities_df = amenities_df.iloc[1:, :]
    amenities_df.set_index("amenity", inplace=True)
    amenities_df.to_csv("amenities_df.csv")


    # linter black
