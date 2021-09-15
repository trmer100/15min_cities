# The openstreetmaps_query is used to gather data from openstreetmaps about amenities in a certain area. This is only used once per month.
import overpy
import pandas as pd
import time


def query(building_type="hospital"):
    """
    this function requests the data for one amenity only in a certain location,
    the output is one dataframe with the exact locations of a certain amenity
    """
    part1 = '[out:json][timeout:50];nwr(51.1238, 6.6824,51.3538, 6.9398)[amenity="'
    part2 = building_type
    part3 = '"];out center;'
    built_query = part1 + part2 + part3
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
    data_frame = pd.DataFrame(list_of_node_tags)
    return data_frame


def data_prep(df):
    """the returned dataframe of the query function cannot be used, therefore the data is prepared for further usage"""
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
    amenities = ["hospital", "dentist", "pharmacy", "school", "kindergarten", "library", "university", "bar", "cafe",
                 "cinema", "fast_food"]
    amenities_raw = pd.Series([""])
    for amenity in amenities:
        storage_df = pd.Series([""])
        storage_df = data_prep(query(building_type=amenity))
        storage_df["amenity"] = pd.Series([amenity for g in range(len(storage_df.index))])
        print(storage_df)
        amenities_raw = pd.concat([amenities_raw, storage_df])
        time.sleep(60)  # sleep timer to avoid "too many requests at the server"
    amenities_df = amenities_raw[["amenity", "latitude", "longitude"]]
    amenities_df = amenities_df.iloc[1:, :]
    amenities_df.set_index("amenity", inplace=True)
    amenities_df.to_csv("amenities_df.csv")
