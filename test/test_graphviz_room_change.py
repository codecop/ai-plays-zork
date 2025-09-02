from test_file_utils import fixture_data_dir  # pylint: disable=unused-import
from graphviz_room_change import GraphvizRoomChange
from map.exploration_action import ExplorationAction


def test_unique_edges(data_dir) -> None:
    gv = GraphvizRoomChange(data_dir)

    gv.record_movement(ExplorationAction("room1", "room2", "north"))
    assert gv.is_graph_updated
    assert len(gv.known_edges) == 1

    gv.record_movement(ExplorationAction("room2", "room1", "south"))
    assert len(gv.known_edges) == 2

    gv.record_movement(ExplorationAction("room1", "room2", "north"))
    gv.record_movement(ExplorationAction("room2", "room1", "south"))
    assert len(gv.known_edges) == 2

    # gv.display()
    # f = data_dir / "map.gv"
    # assert f.exists()
