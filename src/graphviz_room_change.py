from pathlib import Path
from graphviz import Digraph
from map.exploration_action import ExplorationAction
from room_change import RoomChange


class GraphvizRoomChange(RoomChange):
    def __init__(self, run_folder: Path):
        self.g = Digraph("G", filename=run_folder / "map.gv")
        self.edges = set()
        self.g_updated = False

    def record_movement(self, action: ExplorationAction) -> None:
        edge = action.from_room_name + action.to_room_name + str(action.direction)
        if edge not in self.edges:
            self.edges.add(edge)
            self.g.edge(
                action.from_room_name, action.to_room_name, label=str(action.direction)
            )
            self.g_updated = True

            # maybe use ports? plus rank for layout... Code not tested
            # # Direction to port mapping for proper compass arrows
            # direction_ports = {
            #     'north': ('s', 'n'), 'south': ('n', 's'),
            #     'east': ('w', 'e'), 'west': ('e', 'w'),
            #     'up': ('s', 'n'), 'down': ('n', 's')
            # }

            # if action.direction in direction_ports:
            #     from_port, to_port = direction_ports[action.direction]
            #     self.g.edge(f"{action.from_room_name}:{from_port}",
            #                f"{action.to_room_name}:{to_port}",
            #                label=action.direction)
            # else:
            #     self.g.edge(action.from_room_name, action.to_room_name, label=action.direction)

    def display(self) -> None:
        if self.g_updated:
            self.g.view()
            self.g_updated = False
