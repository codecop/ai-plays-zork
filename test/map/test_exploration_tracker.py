from map import ExplorationTracker, GameMap, Room, Exit, ExplorationAction


def test_add_room():
    tracker = ExplorationTracker()
    exits = {"north": Exit("north", None, False)}
    room = Room("kitchen", "A bright kitchen.", exits)

    tracker.add_room(room)

    assert len(tracker.game_map.rooms) == 1
    assert "kitchen" in tracker.game_map.rooms
    assert tracker.game_map.rooms["kitchen"].name == "kitchen"


def test_update_current_room():
    tracker = ExplorationTracker()
    exits = {"south": Exit("south", None, False)}
    room = Room("hall", "A long hallway.", exits)
    tracker.add_room(room)

    tracker.update_current_room("hall")

    assert tracker.game_map.current_room_name == "hall"
    assert len(tracker.game_map.room_history) == 1
    assert tracker.game_map.room_history[0] == "hall"


def test_record_movement():
    tracker = ExplorationTracker()

    hall_exits = {"north": Exit("north", None, False)}
    hall = Room("hall", "A long hallway.", hall_exits)
    kitchen_exits = {"south": Exit("south", None, False)}
    kitchen = Room("kitchen", "A bright kitchen.", kitchen_exits)

    tracker.add_room(hall)
    tracker.add_room(kitchen)
    tracker.update_current_room("hall")

    action = ExplorationAction("hall", "north", "kitchen")
    tracker.record_movement(action)

    hall_room = tracker.get_room_by_name("hall")
    assert hall_room.exits["north"].was_taken is True
    assert hall_room.exits["north"].destination_room_name == "kitchen"
    assert tracker.game_map.current_room_name == "kitchen"


def test_get_unexplored_exits():
    tracker = ExplorationTracker()

    exits1 = {
        "north": Exit("north", None, False),
        "east": Exit("east", "library", True),
    }
    exits2 = {
        "south": Exit("south", None, False),
        "west": Exit("west", None, False),
    }

    room1 = Room("hall", "A hallway.", exits1)
    room2 = Room("study", "A quiet study.", exits2)

    tracker.add_room(room1)
    tracker.add_room(room2)

    unexplored = tracker.get_unexplored_exits()

    assert len(unexplored) == 3
    unexplored_set = set(unexplored)
    assert ("hall", "north") in unexplored_set
    assert ("study", "south") in unexplored_set
    assert ("study", "west") in unexplored_set
    assert ("hall", "east") not in unexplored_set


def test_get_current_unexplored_exits():
    tracker = ExplorationTracker()

    exits = {
        "north": Exit("north", None, False),
        "south": Exit("south", "kitchen", True),
        "east": Exit("east", None, False),
    }
    room = Room("hall", "A hallway.", exits)

    tracker.add_room(room)
    tracker.update_current_room("hall")

    current_unexplored = tracker.get_current_unexplored_exits()

    assert len(current_unexplored) == 2
    assert "north" in current_unexplored
    assert "east" in current_unexplored
    assert "south" not in current_unexplored


def test_get_room_by_name():
    tracker = ExplorationTracker()
    exits = {"up": Exit("up", None, False)}
    room = Room("basement", "A dark basement.", exits)
    tracker.add_room(room)

    found_room = tracker.get_room_by_name("basement")
    missing_room = tracker.get_room_by_name("attic")

    assert found_room is not None
    assert found_room.name == "basement"
    assert missing_room is None


def test_get_current_room():
    tracker = ExplorationTracker()
    exits = {"down": Exit("down", None, False)}
    room = Room("attic", "A dusty attic.", exits)
    tracker.add_room(room)

    current_room_none = tracker.get_current_room()
    tracker.update_current_room("attic")
    current_room = tracker.get_current_room()

    assert current_room_none is None
    assert current_room is not None
    assert current_room.name == "attic"


def test_get_exploration_summary():
    tracker = ExplorationTracker()

    exits1 = {"north": Exit("north", None, False)}
    exits2 = {"south": Exit("south", None, True)}
    room1 = Room("hall", "A hallway.", exits1)
    room2 = Room("kitchen", "A kitchen.", exits2)

    tracker.add_room(room1)
    tracker.add_room(room2)
    tracker.update_current_room("hall")
    tracker.update_current_room("kitchen")
    tracker.update_current_room("hall")

    summary = tracker.get_exploration_summary()

    assert summary["total_rooms_discovered"] == 2
    assert summary["unique_rooms_visited"] == 2
    assert summary["current_room"] == "hall"
    assert summary["unexplored_exits_count"] == 1
    assert summary["room_history_length"] == 3


def test_create_room_from_description():
    tracker = ExplorationTracker()
    directions = ["north", "south", "east"]

    room = tracker.create_room_from_description(
        "garden", "A beautiful garden.", directions
    )

    assert room.name == "garden"
    assert room.description == "A beautiful garden."
    assert len(room.exits) == 3
    assert "north" in room.exits
    assert "south" in room.exits
    assert "east" in room.exits

    for direction in directions:
        exit_obj = room.exits[direction]
        assert exit_obj.direction == direction
        assert exit_obj.destination_room_name is None
        assert exit_obj.was_taken is False
