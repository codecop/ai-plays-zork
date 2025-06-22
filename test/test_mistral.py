import os
from mistralai import Mistral

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-small-latest"  # free


# Try a basic MistralAI connection, see https://docs.mistral.ai/getting-started/clients/
def test_mistral_completion():
    # set MISTRAL_DEBUG=1
    client = Mistral(api_key=api_key)

    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "user",
                "content": "What is the capital of France? Only reply the name, no markup",
            },
        ],
        retries=3,
    )

    assert chat_response.choices[0].message.content == "Paris"


# Try a conversation with an agent and state, see https://docs.mistral.ai/agents/agents_basics/
def test_mistral_agent():
    client = Mistral(api_key=api_key)

    simple_agent = client.beta.agents.create(
        model=model,
        description="A simple Agent with persistent state.",
        name="Test Agent",
        # instructions="You have the ability to perform web searches with `web_search` to find up-to-date information.",
        # tools=[{"type": "web_search"}],
    )

    response = client.beta.conversations.start(
        agent_id=simple_agent.id,
        inputs=[{"role": "user", "content": "Who is Albert Einstein? Just 1 sentence"}],
        # store=False
    )
    print(response.outputs[0].content)

    response = client.beta.conversations.append(
        conversation_id=response.conversation_id,
        inputs="Give another sentence."
    )
    print(response.outputs[0].content)
