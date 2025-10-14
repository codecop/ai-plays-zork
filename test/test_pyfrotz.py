from pyfrotz import Frotz
import pytest
from frotz_patch import patch_frotz


@pytest.fixture(scope="module", autouse=True)
def patch_pyfrotz():
    patch_frotz()


# Use pyfrotz to control a Z-machine interpreter from Python. (curtesy Peter Fichtner)
def test_pyfrotz():

    game = Frotz("frotz/data/zork1.z3")
    game_intro = game.get_intro()
    assert game_intro == ""

    room, description = game.do_command("look")
    assert room.rstrip() == "West of House"
    assert description.startswith(
        "You are standing in an open field west of a white house"
    )

    # while not game.game_ended():
    #     pass

    game.do_command("quit")
    game.do_command("y")

    # close all resources
    game.frotz.stdin.close()
    game.frotz.stdout.close()
    game.frotz.wait()


def test_patched_pyfrotz():
    game = Frotz("frotz/data/zork1.z3")
    game.get_intro()

    assert game.derived_name == "West of House"  # pylint: disable=no-member
    assert game.derived_score == 0  # pylint: disable=no-member
    assert game.derived_moves == 1  # pylint: disable=no-member
    # intro sends an initial look
