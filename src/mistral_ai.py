from mistralai import Mistral
from mistralai.utils import BackoffStrategy, RetryConfig
from ai_interface import AiInterface
import os


api_key = os.environ.get("MISTRAL_API_KEY")
model = "mistral-small-latest"


class MistralAi(AiInterface):

    def __init__(self):
        self.api_key = api_key
        self.model = model

        self.retry_config = RetryConfig(
            "backoff", BackoffStrategy(1, 50, 1.1, 100), True
        )
        self.client = Mistral(
            api_key=self.api_key,
            retry_config=self.retry_config,
        )

        self.agent = None
        self.conversation = None

    def name(self) -> str:
        return "mistralai"

    def start(self, game_notes: str, game_intro: str):
        self.agent = self.client.beta.agents.create(
            model=self.model,
            description="AI adventurer playing Zork.",
            name="Zork Agent",
        )

        # Start conversation with initial prompt
        system_prompt = self.load_resource("system_prompt.md").format(
            game_notes=game_notes, game_intro=game_intro
        )
        self.conversation = self.client.beta.conversations.start(
            agent_id=self.agent.id,
            inputs=[{"role": "user", "content": system_prompt}],
        )

    def get_next_command(self, context: str) -> str:
        if not self.conversation:
            raise ValueError("No active conversation. Call init() first.")

        response = self.client.beta.conversations.append(
            conversation_id=self.conversation.conversation_id,
            inputs=[{"role": "user", "content": context}],
        )

        if response.outputs and len(response.outputs) > 0:
            return response.outputs[0].content
        return "NO RESPONSE"

    def close(self):
        # currently no explicit cleanup needed
        pass
