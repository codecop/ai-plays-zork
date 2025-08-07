from map import Room, Exit, Direction


def test_room_creation():
    exits = {
        Direction.NORTH: Exit(Direction.NORTH, None, False),
        Direction.SOUTH: Exit(Direction.SOUTH, "kitchen", True),
    }
    room = Room("living room", "A cozy living room with a fireplace.", exits)

    assert room.name == "living room"
    assert room.description == "A cozy living room with a fireplace."
    assert len(room.exits) == 2
    assert Direction.NORTH in room.exits
    assert Direction.SOUTH in room.exits


def test_room_add_exit():
    initial_exits = {Direction.NORTH: Exit(Direction.NORTH, None, False)}
    room = Room("hall", "A long hallway.", initial_exits)

    new_exit = Exit(Direction.EAST, "library", False)
    updated_room = room.add_exit(new_exit)

    assert len(updated_room.exits) == 2
    assert Direction.EAST in updated_room.exits
    assert updated_room.exits[Direction.EAST].direction == Direction.EAST
    assert updated_room.exits[Direction.EAST].destination_room_name == "library"
    assert len(room.exits) == 1


def test_room_update_exit():
    exits = {Direction.WEST: Exit(Direction.WEST, None, False)}
    room = Room("study", "A quiet study room.", exits)

    updated_exit = Exit(Direction.WEST, "garden", True)
    updated_room = room.update_exit(Direction.WEST, updated_exit)

    assert updated_room.exits[Direction.WEST].destination_room_name == "garden"
    assert updated_room.exits[Direction.WEST].was_taken is True
    assert room.exits[Direction.WEST].was_taken is False


def test_room_get_exit():
    exits = {Direction.UP: Exit(Direction.UP, "attic", False)}
    room = Room("basement", "A dark basement.", exits)

    exit_obj = room.get_exit(Direction.UP)
    assert exit_obj.direction == Direction.UP
    assert exit_obj.destination_room_name == "attic"

    missing_exit = room.get_exit(Direction.DOWN)
    assert missing_exit is None


def test_room_get_available_directions():
    exits = {
        Direction.NORTH: Exit(Direction.NORTH, "kitchen", False),
        Direction.EAST: Exit(Direction.EAST, None, False),
        Direction.SOUTH: Exit(Direction.SOUTH, "garden", True),
    }
    room = Room("dining room", "A formal dining room.", exits)

    directions = room.get_available_directions()
    assert len(directions) == 3
    assert Direction.NORTH in directions
    assert Direction.EAST in directions
    assert Direction.SOUTH in directions


def test_room_get_unexplored_exits():
    exits = {
        Direction.NORTH: Exit(Direction.NORTH, "kitchen", True),
        Direction.EAST: Exit(Direction.EAST, None, False),
        Direction.SOUTH: Exit(Direction.SOUTH, "garden", False),
        Direction.WEST: Exit(Direction.WEST, "library", True),
    }
    room = Room("center hall", "The central hall.", exits)

    unexplored = room.get_unexplored_exits()
    assert len(unexplored) == 2

    unexplored_directions = [exit.direction for exit in unexplored]
    assert Direction.EAST in unexplored_directions
    assert Direction.SOUTH in unexplored_directions
    assert Direction.NORTH not in unexplored_directions
    assert Direction.WEST not in unexplored_directions
