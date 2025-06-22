import os
from mistralai import Mistral

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-small-latest"  # free


# Try a MistralAI connection, see https://docs.mistral.ai/getting-started/clients/
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
