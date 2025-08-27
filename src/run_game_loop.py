import re
import time
from ai_interface import AiInterface
from game import Game
from map.exploration_action import ExplorationAction
from map.exploration_tracker import ExplorationTracker


def run(ai: AiInterface, threshold: float = 0) -> None:
    """Run the game loop with a given AI."""
    log = ai.log  # reuse same logger

    # start game
    game = Game()
    game_notes = game.get_game_play_notes()
    game_intro = game.get_intro()

    tracker = ExplorationTracker()

    ai.start(game_notes, game_intro)

    # run loop
    start_time = time.time()
    command = "look"
    current_room = None
    while True:
        # TODO write all AI commands to a separate log in the run folder
        game_output = game.do_command(command)
        log.game(game_output)

        if current_room != None and current_room != game.room_name():
            log.room(game.room_name())
            # we moved
            with open('commands.txt', 'a') as f:
                f.write(command + '\n')

            directions = ["north", "south", "east", "west", "northeast", "northwest", "southeast", "southwest", "up", "down"]
            direction_regex = "|".join(directions)
            direction_regex = "(" + direction_regex + ")"
            match = re.match(direction_regex, command, re.IGNORECASE)
            if match:
                direction = match.group(1)
                direction = direction.lower()
            else:
                direction = command
                # special cases:
                # enter window
                # climb tree
            # print(direction)

            # track movement
            action = ExplorationAction(
                current_room,
                direction,
                game.room_name()
            )
            tracker.record_movement(action)
            
        current_room = game.room_name()

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
