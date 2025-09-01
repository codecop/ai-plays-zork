import time
from pathlib import Path
from ai_interface import AiInterface
from command_log import CommandLog
from game import Game
from graphviz_room_change import GraphvizRoomChange
from log import Log
from room_change_tracker import RoomChangeTracker


def run(run_folder: Path, log: Log, ai: AiInterface, threshold: float = 0) -> None:
    """Run the game loop with a given AI."""

    # start game
    game = Game()
    game_notes = game.get_game_play_notes()
    game_intro = game.get_intro()

    tracker = RoomChangeTracker(
        GraphvizRoomChange(run_folder), log, CommandLog(run_folder, "move_")
    )

    ai.start(game_notes, game_intro)

    # run loop
    start_time = time.time()
    command = "look"
    while True:
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
