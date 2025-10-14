from frotz.game import Game


def test_game_formatting():

    game = Game()
    game.get_intro()

    description = game.do_command("look")
    assert description == (
        "West of House\n"
        + "You are standing in an open field west of a white house, with a boarded front door. "
        + "There is a small mailbox here."
    )
    assert game.room_name() == "West of House"

    game.quit()
    game.close()


def test_game_errors():

    game = Game()
    assert game.get_intro() == ""

    description = game.do_command("foo")
    assert description == 'I don\'t know the word "foo".'

    assert game.game_ended() is False

    # no game.quit()
    game.close()
