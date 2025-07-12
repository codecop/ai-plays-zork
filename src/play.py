import os
from file_utils import getNextFolderName, readGamePlayNotes
from log import Log
from pyfrotz import Frotz
from mistralai import Mistral

ai = "mistralai"

# create run
baseName = f"{ai}-run"
folderName = getNextFolderName(".", baseName)
log = Log(folderName + "/log.txt")

# start game
game = Frotz("data/zork1.z3")
game_intro = game.get_intro()
game_notes = readGamePlayNotes()

# init ai
key_name = "MISTRAL_API_KEY"
api_key = os.environ[key_name]
model = "mistral-small-latest"  # free
client = Mistral(api_key=api_key)

zork_agent = client.beta.agents.create(
    model=model,
    description="AI adventurer playing Zork.",
    name="Zork Agent",
    # instructions="You have the ability to perform web searches with `web_search` to find up-to-date information.",
    # tools=[{"type": "web_search"}],
)

response = client.beta.conversations.start(
    agent_id=zork_agent.id,
    inputs=[
        {
            "role": "system",
            "content": "You're an AI adventurer playing Zork. Zork is a text based turn based game.\nWe want you to play it and figure out how you want to keep track of your progress and current state.",
        },
        {"role": "user", "content": game_notes},
    ],
    # store=False
)

# run loop
command = "look"
while True:
    room, description = game.do_command(command)
    log.room(room)
    log.gameText(description)

    # pass to ai
    context = f"You are in {room}.\n {description}"
    response = client.beta.conversations.append(
        conversation_id=response.conversation_id,
        inputs=[
            {
                "role": "system",
                "content": "You're an AI adventurer playing Zork. Zork is a text based turn based game.\nWe want you to play it and figure out how you want to keep track of your progress and current state.",
            },
            {"role": "user", "content": context},
        ],
    )
    command = response.outputs[0].content
    log.command(command)

    if game.game_ended():
        break

# game.do_command("quit")
# game.do_command("y")

# close AI

# close game resources
game.frotz.stdin.close()
game.frotz.stdout.close()
game.frotz.wait()

# TODO maybe save statistics
