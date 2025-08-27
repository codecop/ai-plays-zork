from typing import List, Tuple, Optional, Dict
from .game_map import GameMap
from .room import Room
from .exit import Exit, Direction
from .exploration_action import ExplorationAction
from graphviz import Digraph


class ExplorationTracker:
    def __init__(self, game_map: Optional[GameMap] = None):
        self.g = Digraph("G", filename="map.gv")
        self.edges = set()
        self.g_updated = False
        self.game_map = game_map or GameMap()

    def add_room(self, room: Room) -> None:
        self.game_map.add_room(room)

    def update_current_room(self, room_name: str) -> None:
        self.game_map.set_current_room(room_name)

    def record_movement(self, action: ExplorationAction) -> None:
        edge = action.from_room_name + action.to_room_name + action.direction
        if edge not in self.edges:
            self.edges.add(edge)
            self.g.edge(action.from_room_name, action.to_room_name, label=action.direction)
            self.g_updated = True

        # TODO not working as it does not create new rooms on the first hit?
        from_room = self.game_map.get_room(action.from_room_name)
        if from_room and action.direction in from_room.exits:
            exit_obj = from_room.exits[action.direction]
            updated_exit = exit_obj.mark_as_taken().set_destination(action.to_room_name)
            updated_room = from_room.update_exit(action.direction, updated_exit)
            self.game_map.update_room(updated_room)

        self.update_current_room(action.to_room_name)

    def get_unexplored_exits(self) -> List[Tuple[str, Direction]]:
        unexplored = []
        for room_name, room in self.game_map.rooms.items():
            for direction, exit_obj in room.exits.items():
                if not exit_obj.was_taken:
                    unexplored.append((room_name, direction))
        return unexplored

    def get_current_unexplored_exits(self) -> List[Direction]:
        current_room = self.get_current_room()
        if not current_room:
            return []
        return [
            direction
            for direction, exit_obj in current_room.exits.items()
            if not exit_obj.was_taken
        ]

    def get_room_by_name(self, room_name: str) -> Optional[Room]:
        return self.game_map.get_room(room_name)

    def get_current_room(self) -> Optional[Room]:
        return self.game_map.get_current_room()

    def get_exploration_summary(self) -> Dict:
        total_rooms = len(self.game_map.rooms)
        unique_rooms_visited = len(set(self.game_map.room_history))
        unexplored_exits = len(self.get_unexplored_exits())

        return {
            "total_rooms_discovered": total_rooms,
            "unique_rooms_visited": unique_rooms_visited,
            "current_room": self.game_map.current_room_name,
            "unexplored_exits_count": unexplored_exits,
            "room_history_length": len(self.game_map.room_history),
        }

    def create_room_from_description(
        self, name: str, description: str, available_directions: List[Direction]
    ) -> Room:
        exits = {}
        for direction in available_directions:
            exits[direction] = Exit(
                direction=direction, destination_room_name=None, was_taken=False
            )

        return Room(name=name, description=description, exits=exits)

    def render_map(self) -> None:
        if self.g_updated:
            self.g.view()
            self.g_updated = False
