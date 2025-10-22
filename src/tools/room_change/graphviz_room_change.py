from pathlib import Path
from graphviz import Digraph
from tools.room_change.exploration_action import ExplorationAction
from tools.room_change.room_change import RoomChange


DIRECTION_PORTS = {
    "north": ("n", "s"),
    "east": ("e", "w"),
    "south": ("s", "n"),
    "west": ("w", "e"),
    "northeast": ("ne", "sw"),
    "southeast": ("se", "nw"),
    "southwest": ("sw", "ne"),
    "northwest": ("nw", "se"),
}


class GraphvizRoomChange(RoomChange):
    """Draw the map of visited new rooms using Graphviz."""

    def __init__(self, path: Path, view: bool = True):
        path.mkdir(parents=True, exist_ok=True)
        self.view = view
        filename = path / "map.gv"
        self.g = Digraph("G", filename=filename)
        self.known_edges = set()
        self.is_graph_updated = False

    def record_movement(self, action: ExplorationAction) -> None:
        edge = f"{action.from_room_name}-{action.to_room_name}-{action.direction}"
        if edge not in self.known_edges:
            self.known_edges.add(edge)

            if action.direction in DIRECTION_PORTS:
                from_port, to_port = DIRECTION_PORTS[action.direction]
                self.g.edge(
                    f"{action.from_room_name}:{from_port}",
                    f"{action.to_room_name}:{to_port}",
                    label=action.direction,
                )
            else:
                self.g.edge(
                    action.from_room_name, action.to_room_name, label=action.direction
                )
            self.is_graph_updated = True

    def display(self) -> None:
        if self.is_graph_updated:
            if self.view:
                self.g.view()
            else:
                self.g.save()
            self.is_graph_updated = False
