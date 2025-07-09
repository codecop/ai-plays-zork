import os
from mistralai import Mistral

key_name = "MISTRAL_API_KEY"
api_key = os.environ[key_name]
model = "mistral-small-latest"  # free

client = Mistral(api_key=api_key)

agents = client.beta.agents.list()
for agent in agents:
    print("deleting " + agent.name)
    # client.beta.agents.delete(agent_id=agent.id)
