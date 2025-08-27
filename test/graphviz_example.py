from graphviz import Digraph

# Compass-aligned directions using ports
g = Digraph("CompassMap", filename="compass_map.gv")

# how to name the edges
# g.edge("West of House", "Woods", label="north")
# g.edge("Woods", "West of House", label="south")

# shape the rooms, not needed
# g.node("Center", shape="box")
# g.node("North_Room", shape="box")

# place port in proper direction
# Use ports to make arrows point in compass directions:
# :n = north port, :s = south port, :e = east port, :w = west port
g.edge("Center:n", "North_Room:s", label="north")   # arrow points UP
# g.edge("North_Room:s", "Center:n", label="south")


g.view()
