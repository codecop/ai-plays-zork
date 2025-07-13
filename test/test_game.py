from game import Game


def test_game_formatting():

    game = Game()
    game.get_intro()

    description = game.do_command("look")
    assert description == (
        "West of House\n"
        + "You are standing in an open field west of a white house, with a boarded front door. "
        + "There is a small mailbox here."
    )

    game.quit()

    game.close()
