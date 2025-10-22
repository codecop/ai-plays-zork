from tools.room_change.graphviz_room_change import GraphvizRoomChange
from tools.room_change.exploration_action import ExplorationAction
from util.file_utils import read_file


def test_unique_edges(data_dir) -> None:
    gv = GraphvizRoomChange(data_dir, False)

    gv.record_movement(ExplorationAction("room1", "room2", "north"))
    assert gv.is_graph_updated
    assert len(gv.known_edges) == 1

    gv.record_movement(ExplorationAction("room2", "room1", "south"))
    assert len(gv.known_edges) == 2

    gv.record_movement(ExplorationAction("room1", "room2", "north"))
    gv.record_movement(ExplorationAction("room2", "room1", "south"))
    assert len(gv.known_edges) == 2


def test_graph_file(data_dir) -> None:
    gv = GraphvizRoomChange(data_dir, False)
    gv.record_movement(ExplorationAction("southern room", "north", "northern room"))

    gv.display()
    actual_file = data_dir / "map.gv"
    assert actual_file.exists()
    # assert (data_dir / "map.gv.pdf").exists()

    expected_file = "test/data/graphviz_room_change/single.gv"
    expected_content = read_file(expected_file)

    actual_content = read_file(actual_file)
    assert actual_content == expected_content
