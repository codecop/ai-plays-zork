import time
from ai_interface import AiInterface
from game import Game
from room_change_tracker import RoomChangeTracker
from graphviz_room_change import GraphvizRoomChange


def run(ai: AiInterface, threshold: float = 0) -> None:
    """Run the game loop with a given AI."""
    log = ai.log  # reuse same logger

    # start game
    game = Game()
    game_notes = game.get_game_play_notes()
    game_intro = game.get_intro()

    tracker = RoomChangeTracker(GraphvizRoomChange(ai.run_folder), ai.log, debug=True)

    ai.start(game_notes, game_intro)

    # run loop
    start_time = time.time()
    command = "look"
    while True:
        # TODO write all AI commands to a separate log in the run folder
        game_output = game.do_command(command)
        log.game(game_output)

        tracker.check_for_movement(game.room_name(), command)

        # wait for threshold
        elapsed_time = time.time() - start_time
        if elapsed_time < threshold:
            time.sleep(threshold - elapsed_time)

        start_time = time.time()

        # Get AI's next move
        command = ai.get_next_command(game_output)
        log.command(command)

        if game.game_ended():
            break

    # close all
    ai.close()
    game.close()
