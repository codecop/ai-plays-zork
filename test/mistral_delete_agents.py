import os
from mistralai import Mistral

key_name = "MISTRAL_API_KEY"
api_key = os.environ[key_name]
model = "mistral-small-latest"  # free

client = Mistral(api_key=api_key)

agents = client.beta.agents.list()
agents.sort(key=lambda agent: agent.created_at)
print("found %s agents" % len(agents))
# it's always 20 agents, so it will not keep more than that
for agent in agents:
    print("deleting %s from %s" % (agent.name, agent.created_at))
    # client.beta.agents.delete(agent_id=agent.id)
