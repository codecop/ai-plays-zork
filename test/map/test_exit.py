from map import Exit, Direction


def test_exit_creation():
    exit_obj = Exit(Direction.NORTH, "kitchen", False)

    assert exit_obj.direction == Direction.NORTH
    assert exit_obj.destination_room_name == "kitchen"
    assert exit_obj.was_taken is False


def test_exit_creation_with_defaults():
    exit_obj = Exit(Direction.SOUTH, None)

    assert exit_obj.direction == Direction.SOUTH
    assert exit_obj.destination_room_name is None
    assert exit_obj.was_taken is False


def test_exit_mark_as_taken():
    exit_obj = Exit(Direction.EAST, "library", False)
    taken_exit = exit_obj.mark_as_taken()

    assert taken_exit.was_taken is True
    assert taken_exit.direction == Direction.EAST
    assert taken_exit.destination_room_name == "library"
    assert exit_obj.was_taken is False


def test_exit_set_destination():
    exit_obj = Exit(Direction.WEST, None, False)
    updated_exit = exit_obj.set_destination("garden")

    assert updated_exit.destination_room_name == "garden"
    assert updated_exit.direction == Direction.WEST
    assert updated_exit.was_taken is False
    assert exit_obj.destination_room_name is None
