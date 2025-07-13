from pathlib import Path
from mistralai import Mistral
from mistralai.utils import BackoffStrategy, RetryConfig
from ai_interface import AiInterface
from log import Log
import os


api_key = os.environ.get("MISTRAL_API_KEY")
model = "mistral-small-latest"


class MistralAi(AiInterface):

    def __init__(self, configuration: str, run_folder: Path, log: Log):
        super().__init__(configuration, run_folder, log)

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
        self.conversation_id = None
        self.calls = 0

    def start(self, game_notes: str, game_intro: str) -> None:
        self.system_prompt = self.load_resource("system_prompt.md").format(
            game_notes=game_notes, game_intro=game_intro
        )

        self.agent = self.client.beta.agents.create(
            model=self.model,
            description="AI adventurer playing Zork.",
            name="Zork Agent",
            instructions=self.system_prompt,
        )

        self.log.ai(
            f"ai: {self.__class__}\n"
            + f"configuration: {self.configuration}\n"
            + f"model: {self.model}\n"
            + f"agent id: {self.agent.id}"
        )
        self.write_run_resource("system_prompt.md", self.system_prompt)

    def get_next_command(self, context: str) -> str:
        if not self.conversation_id:
            response = self.client.beta.conversations.start(
                agent_id=self.agent.id,
                inputs=[{"role": "user", "content": context}],
            )
            self.conversation_id = response.conversation_id
        else:
            response = self.client.beta.conversations.append(
                conversation_id=self.conversation_id,
                inputs=[{"role": "user", "content": context}],
            )

        self.calls += 1
        if response.outputs and len(response.outputs) > 0:
            result = response.outputs[0].content
            if "\n" in result:
                self.log.ai(result)
                result = result.splitlines()[-1]
            return result
        self.log.ai("NO RESPONSE")
        return "NO RESPONSE"

    def close(self) -> None:
        # currently no explicit cleanup needed
        pass
