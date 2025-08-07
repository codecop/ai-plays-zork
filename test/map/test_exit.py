from map import Exit


def test_exit_creation():
    exit_obj = Exit("north", "kitchen", False)

    assert exit_obj.direction == "north"
    assert exit_obj.destination_room_name == "kitchen"
    assert exit_obj.was_taken is False


def test_exit_creation_with_defaults():
    exit_obj = Exit("south", None)

    assert exit_obj.direction == "south"
    assert exit_obj.destination_room_name is None
    assert exit_obj.was_taken is False


def test_exit_mark_as_taken():
    exit_obj = Exit("east", "library", False)
    taken_exit = exit_obj.mark_as_taken()

    assert taken_exit.was_taken is True
    assert taken_exit.direction == "east"
    assert taken_exit.destination_room_name == "library"
    assert exit_obj.was_taken is False


def test_exit_set_destination():
    exit_obj = Exit("west", None, False)
    updated_exit = exit_obj.set_destination("garden")

    assert updated_exit.destination_room_name == "garden"
    assert updated_exit.direction == "west"
    assert updated_exit.was_taken is False
    assert exit_obj.destination_room_name is None


def test_exit_method_chaining():
    exit_obj = Exit("up", None, False)
    final_exit = exit_obj.set_destination("attic").mark_as_taken()

    assert final_exit.destination_room_name == "attic"
    assert final_exit.was_taken is True
    assert final_exit.direction == "up"
    assert exit_obj.was_taken is False
    assert exit_obj.destination_room_name is None


def test_exit_immutability():
    exit_obj = Exit("north", None, False)
    taken_exit = exit_obj.mark_as_taken()
    destination_exit = exit_obj.set_destination("kitchen")

    assert exit_obj.was_taken is False
    assert exit_obj.destination_room_name is None
    assert taken_exit.was_taken is True
    assert destination_exit.destination_room_name == "kitchen"
