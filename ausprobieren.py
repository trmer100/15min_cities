import pandas as pd
from grid2 import cells  # this will transfer the output from grid2 to this script
dfcells = pd.DataFrame.from_dict(cells)
print(dfcells)



from scipy import spatial
point = (51.2290062, 6.8212808624507195)
airports = [(50.22,6.77),(51.33,8.77),(49.2256,6.88897),(55.1123,6.11231)]
tree = spatial.KDTree(airports)
print(tree.query([(49.2290062,6.8212808624507195)]))
#(array([ 1.41421356]), array([1]))