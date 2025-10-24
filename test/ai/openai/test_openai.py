import os
import pytest
from openai import OpenAI
from agents import Agent, Runner

# Skip all tests if API key is not set
KEY_NAME = "OPENAI_API_KEY"
if KEY_NAME not in os.environ:
    pytest.skip(KEY_NAME + " variable not set", allow_module_level=True)

api_key = os.environ[KEY_NAME]
MODEL = "gpt-4.1-nano"  # "gpt-4.1-mini" # "gpt-4.1"


# see https://platform.openai.com/docs/api-reference/chat/create
def test_openai_completion():
    client = OpenAI(api_key=api_key)

    chat_response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "developer", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": "What is the capital of France? Only reply the name, no markup",
            },
        ],
    )

    assert chat_response.choices[0].message.content == "Paris"


# # see https://platform.openai.com/docs/api-reference/assistants/createAssistant
# def test_openai_agent():
#     client = OpenAI(api_key=api_key)

#     simple_agent = client.beta.assistants.create(
#         model=MODEL,
#         name="Test Agent",
#         description="A unit test Agent with persistent state.",
#     )
#     print(simple_agent)

#     thread = client.beta.threads.create(
#         assistant_id=simple_agent.id,
#         # inputs=[{"role": "user", "content": "Who is Albert Einstein? Just 1 sentence"}],
#         # store=False
#     )
#     assert len(response.outputs) == 1
#     print(response.outputs[0].content)

#     response = client.beta.conversations.append(
#         conversation_id=response.conversation_id, inputs="Give another sentence."
#     )
#     assert len(response.outputs) == 1
#     print(response.outputs[0].content)


# see https://github.com/openai/openai-agents-python/blob/main/examples/basic/hello_world.py
@pytest.mark.asyncio
async def test_openai_agent():
    simple_agent = Agent(
        model=MODEL,
        name="Test Agent",
        # instructions="You only respond in haikus.",
    )
    # print(simple_agent)

    result = await Runner.run(simple_agent, "Who is Albert Einstein? Just 1 sentence")
    # print(result)
    print("\n  1: " + result.final_output)
    # assert "abc" == result.final_output

    new_input = result.to_input_list() + [
        {"role": "user", "content": "Give another sentence."}
    ]
    result = await Runner.run(simple_agent, new_input)
    print("  2: " + result.final_output, end="")
    # assert "abc" == result.final_output
