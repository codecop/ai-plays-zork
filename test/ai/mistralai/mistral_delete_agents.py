import os
from mistralai import Mistral

KEY_NAME = "MISTRAL_API_KEY"
api_key = os.environ[KEY_NAME]

client = Mistral(api_key=api_key)

agents = client.beta.agents.list()
agents.sort(key=lambda agent: agent.created_at)
print(f"found {len(agents)} agents")
# it's always 20 agents, so it will not keep more than that
for agent in agents:
    print(f"deleting {agent.name} from {agent.created_at}")
    # client.beta.agents.delete(agent_id=agent.id)
