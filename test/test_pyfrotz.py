from pyfrotz import Frotz


# Use pyfrotz to control a Z-machine interpreter from Python. (curtesy Peter Fichtner)
def test_pyfrotz():

    game = Frotz("data/zork1.z3")
    game_intro = game.get_intro()

    room, description = game.do_command("look")
    assert room.rstrip() == "West of House"

    # while not game.game_ended():
    #     pass

    game.do_command("quit")
    game.do_command("y")

    # close all resources
    game.frotz.stdin.close()
    game.frotz.stdout.close()
    game.frotz.wait()
