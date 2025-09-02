import json
import os
import pytest
from mistralai import Mistral

# Skip all tests if API key is not set
KEY_NAME = "MISTRAL_API_KEY"
if KEY_NAME not in os.environ:
    pytest.skip(KEY_NAME + " variable not set", allow_module_level=True)

api_key = os.environ[KEY_NAME]
MODEL = "mistral-small-latest"  # free


# Try a basic MistralAI connection, see https://docs.mistral.ai/getting-started/clients/
def test_mistral_completion():
    # set MISTRAL_DEBUG=1
    client = Mistral(api_key=api_key)

    chat_response = client.chat.complete(
        model=MODEL,
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
        model=MODEL,
        description="A unit test Agent with persistent state.",
        name="Test Agent",
    )

    response = client.beta.conversations.start(
        agent_id=simple_agent.id,
        inputs=[{"role": "user", "content": "Who is Albert Einstein? Just 1 sentence"}],
        # store=False
    )
    assert len(response.outputs) == 1
    print(response.outputs[0].content)

    response = client.beta.conversations.append(
        conversation_id=response.conversation_id, inputs="Give another sentence."
    )
    assert len(response.outputs) == 1
    print(response.outputs[0].content)


def identify_user(user_id: str) -> str:
    if user_id == "U128":
        return "Hans"
    assert False


# Try using tools, see https://docs.mistral.ai/capabilities/function_calling/
def test_mistral_function_calling():
    client = Mistral(api_key=api_key)

    simple_agent = client.beta.agents.create(
        model=MODEL,
        description="A unit test Agent with functions.",
        name="Test Function Calling Agent",
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "identify_user",
                    "description": "Get user name from user id",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "string",
                                "description": "The user id.",
                            }
                        },
                        "required": ["user_id"],
                    },
                },
            },
        ],
    )

    response = client.beta.conversations.start(
        agent_id=simple_agent.id,
        inputs=[
            {
                "role": "user",
                "content": 'Who is user U128? Return the sentence "User U128 is %s"',
            }
        ],
    )
    assert len(response.outputs) == 1
    output = response.outputs[0]
    # Union[ToolExecutionEntry, FunctionCallEntry, MessageOutputEntry, AgentHandoffEntry]
    assert output.type == "function.call"

    # eval function
    function_name = output.name
    function_args = json.loads(output.arguments)
    assert function_name == "identify_user"
    assert function_args == {"user_id": "U128"}
    function_result = globals()[function_name](**function_args)
    assert function_result == "Hans"

    response = client.beta.conversations.append(
        conversation_id=response.conversation_id,
        # List[MessageInputEntry|FunctionResultEntry]
        inputs=[
            {
                "tool_call_id": output.tool_call_id,
                "result": function_result,
            }
        ],
    )

    assert len(response.outputs) == 1
    output = response.outputs[0]
    assert output.type == "message.output"
    print(output.content)
    assert output.content == "User U128 is Hans"
