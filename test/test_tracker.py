from tracker import Tracker


def test_x() -> None:
    t = Tracker()

    result = t.get_room_from_description(
        """West of House
You are standing in an open field west of a white house, with a boarded
front door."""
    )

    # TODO assert result == "West of House"
    assert result is None
