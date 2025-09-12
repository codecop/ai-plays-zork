import pytest
from graphviz import Digraph


@pytest.mark.skip("Graphviz example is manual")
def test_graphviz_graph_example() -> None:
    g = Digraph("Example", filename="./.pytest_cache/example.gv")

    # how to name the edges
    g.edge("West of House", "Woods", label="north")
    g.edge("Woods", "West of House", label="south")

    # shape the rooms, not needed
    g.node("Woods", shape="box")

    g.view()


@pytest.mark.skip("Graphviz example is manual")
def test_graphviz_port_example() -> None:
    g = Digraph("Ports", filename="./.pytest_cache/ports.gv")

    # place port in proper direction:
    # :n = north port, :s = south port, :e = east port, :w = west port
    g.edge("Center:n", "North_Room:s", label="north")  # arrow points UP

    g.view()
