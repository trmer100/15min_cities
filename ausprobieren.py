from grid2 import cells  # this will transfer the output from grid2 to this script
from scipy import spatial
listcells = list(cells.keys())
point = (51.2290062, 6.8212808624507195)
tree = spatial.KDTree(listcells)
print(tree.query([point]))
