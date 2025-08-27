# import graphviz
from graphviz import Digraph

g = Digraph("G", filename="map.gv")

# edges with directions/labels
g.edge("Hello", "World", label="Edge Label 1")
g.edge("Hello 2", "World 2", dir="back", label="Edge Label 2")
g.edge("Hello 3", "World 3", dir="both", label="Edge Label 3")

# a room has an exit and it goes back the same direction
g.edge("West of House", "Woods", label="north")
g.edge("Woods", "West of House", label="south")

g.view()
