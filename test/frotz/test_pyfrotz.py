from pyfrotz import Frotz
import pytest
from frotz.frotz_patch import patch_frotz


@pytest.fixture(scope="module", autouse=True)
def patch_pyfrotz():
    patch_frotz()


@pytest.fixture(name="new_game")
def fixture_new_game():
    game = Frotz("frotz/data/zork1.z3")

    yield game

    game.do_command("quit")
    game.do_command("y")
    # close all resources
    game.frotz.stdin.close()
    game.frotz.stdout.close()
    game.frotz.wait()


# Use pyfrotz to control a Z-machine interpreter from Python. (curtesy Peter Fichtner)
def test_pyfrotz(new_game):
    game_intro = new_game.get_intro()
    assert game_intro == ""

    room, description = new_game.do_command("look")
    assert room.rstrip() == "West of House"
    assert description.startswith(
        "You are standing in an open field west of a white house"
    )

    # while not game.game_ended():
    #     pass


def test_patched_pyfrotz(new_game):
    new_game.get_intro()

    # intro sends an initial look
    assert new_game.derived_name == "West of House"
    assert new_game.derived_score == 0
    assert new_game.derived_moves == 1

    new_game.do_command("look")
    assert new_game.derived_score == 0
    assert new_game.derived_moves == 2
