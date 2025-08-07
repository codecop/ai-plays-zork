from map import Room, Exit


def test_room_creation():
    exits = {
        "north": Exit("north", None, False),
        "south": Exit("south", "kitchen", True),
    }
    room = Room("living room", "A cozy living room with a fireplace.", exits)

    assert room.name == "living room"
    assert room.description == "A cozy living room with a fireplace."
    assert len(room.exits) == 2
    assert "north" in room.exits
    assert "south" in room.exits


def test_room_add_exit():
    initial_exits = {"north": Exit("north", None, False)}
    room = Room("hall", "A long hallway.", initial_exits)

    new_exit = Exit("east", "library", False)
    updated_room = room.add_exit(new_exit)

    assert len(updated_room.exits) == 2
    assert "east" in updated_room.exits
    assert updated_room.exits["east"].direction == "east"
    assert updated_room.exits["east"].destination_room_name == "library"
    assert len(room.exits) == 1


def test_room_update_exit():
    exits = {"west": Exit("west", None, False)}
    room = Room("study", "A quiet study room.", exits)

    updated_exit = Exit("west", "garden", True)
    updated_room = room.update_exit("west", updated_exit)

    assert updated_room.exits["west"].destination_room_name == "garden"
    assert updated_room.exits["west"].was_taken is True
    assert room.exits["west"].was_taken is False


def test_room_get_exit():
    exits = {"up": Exit("up", "attic", False)}
    room = Room("basement", "A dark basement.", exits)

    exit_obj = room.get_exit("up")
    assert exit_obj.direction == "up"
    assert exit_obj.destination_room_name == "attic"

    missing_exit = room.get_exit("down")
    assert missing_exit is None


def test_room_get_available_directions():
    exits = {
        "north": Exit("north", "kitchen", False),
        "east": Exit("east", None, False),
        "south": Exit("south", "garden", True),
    }
    room = Room("dining room", "A formal dining room.", exits)

    directions = room.get_available_directions()
    assert len(directions) == 3
    assert "north" in directions
    assert "east" in directions
    assert "south" in directions


def test_room_get_unexplored_exits():
    exits = {
        "north": Exit("north", "kitchen", True),
        "east": Exit("east", None, False),
        "south": Exit("south", "garden", False),
        "west": Exit("west", "library", True),
    }
    room = Room("center hall", "The central hall.", exits)

    unexplored = room.get_unexplored_exits()
    assert len(unexplored) == 2

    unexplored_directions = [exit.direction for exit in unexplored]
    assert "east" in unexplored_directions
    assert "south" in unexplored_directions
    assert "north" not in unexplored_directions
    assert "west" not in unexplored_directions


def test_room_immutability():
    exits = {"north": Exit("north", None, False)}
    room = Room("original", "Original description", exits)

    new_exit = Exit("south", "kitchen", False)
    updated_room = room.add_exit(new_exit)

    assert len(room.exits) == 1
    assert len(updated_room.exits) == 2
    assert room.name == "original"
    assert updated_room.name == "original"
