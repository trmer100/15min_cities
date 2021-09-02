#run in python console to install overpy package: "pip install requests"

import overpy
import pandas as pd
import time

def query(building_type):
    part1 = '[out:json][timeout:50];nwr(51.1238, 6.6824,51.3538, 6.9398)[amenity="'
    part2 = building_type
    part3 = '"];out center;'
    built_query = part1 + part2 + part3
    print(built_query)
   # UL = ('51.3538', '6.6824')
   # UR = ('51.3538', '6.9398')
   # LL = ('51.1238', '6.6824')
   # LR = ('51.1238', '6.9398')



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
    #df.set_index("name",inplace=True)
    df_global_reduced= df[["name","latitude","longitude"]]
    df_global_reduced_float = df_global_reduced.copy()
    df_global_reduced_float["latitude"] = df_global_reduced_float["latitude"].astype("float")
    df_global_reduced_float["longitude"] = df_global_reduced_float["longitude"].astype("float")
    assert df_global_reduced_float["latitude"].dtype == "float"
    assert df_global_reduced_float["longitude"].dtype == "float"
    return df_global_reduced_float

#amenities = ["hospital","school","bar","cafe","fast_food","college","kindergarten"] #insert the amenities here
#amenities = ["cafe","fast_food"]
amenities = ["hospital","school","kindergarten"]

dfObj = [] #empty df which is used for storing the data from the for loop below
df1 = pd.Series([""]) #empty series to use "concat" in the for loop
for x in amenities:
    df2= pd.Series([""])
    df2 = data_prep(query(x))
    df2["amenity"] = pd.Series([x for g in range(len(df2.index))])
    print(df2)
    df1 = pd.concat([df1,df2])
    time.sleep(30) #sleep timer to avoid "too many requests at the server"


dfshort = df1[["amenity","latitude","longitude"]]
dfshort = dfshort.iloc[1:,:]

dfshort.set_index("amenity",inplace=True)
print(dfshort)

#dfshort.to_csv(r'C:\Users\pmard\Desktop\TEST OUTPUT\dfshort_output.csv')
dfshort.to_csv("dfshort_output.csv")
#dfsoloa = dfshort.filter(like="hospital",axis = 0)
#dfsolob = dfshort.filter(like="school",axis = 0)
#dfsoloa = dfshort[["hospital"]]
#dfsolob = dfshort[["school"]]
#print(dfsoloa)
#print(dfsolob)
#dfsoloa.to_csv("output_dfsoloa.csv")
#dfsolob.to_csv("output_dfsolob.csv")
