from pathlib import Path
from mistralai import Mistral
from mistralai.utils import BackoffStrategy, RetryConfig
from ai_interface import AiInterface
from log import Log
import os


api_key = os.environ.get("MISTRAL_API_KEY")


class MistralAi(AiInterface):

    def __init__(self, configuration: str, run_folder: Path, log: Log):
        super().__init__(configuration, run_folder, log)

        self.api_key = api_key

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
        system_prompt = self.load_resource("system_prompt.md").format(
            game_notes=game_notes, game_intro=game_intro
        )

        self.agent = self.client.beta.agents.create(
            model=self.config()["model"],
            description=self.config()["description"],
            name=self.config()["name"],
            instructions=system_prompt,
        )

        self.log.ai(
            f"ai: {self.__class__}\n"
            + f"configuration: {self.configuration}\n"
            + f"model: {self.agent.model}\n"
            + f"agent id: {self.agent.id}\n"
            + f"name: {self.agent.name}\n"
            + f"description: {self.agent.description}"
        )
        self.write_run_resource("system_prompt.md", system_prompt)

    def get_next_command(self, context: str) -> str:
        prompt = f"Game answers with {context}"
        if not self.conversation_id:
            response = self.client.beta.conversations.start(
                agent_id=self.agent.id,
                inputs=[{"role": "user", "content": prompt}],
            )
            self.conversation_id = response.conversation_id
        else:
            response = self.client.beta.conversations.append(
                conversation_id=self.conversation_id,
                inputs=[{"role": "user", "content": prompt}],
            )

        self.calls += 1
        if response.outputs and len(response.outputs) > 0:
            if len(response.outputs) > 1:
                self.log.ai("WARN multiple responses " + str(response.outputs))

            output = response.outputs[0]
            if output.type == "message.output":
                result = output.content
            else:
                self.log.ai("WARN not a message response " + str(output))
                return "NO RESPONSE"

            if "\n" in result:
                self.log.ai(result)
                result = result.splitlines()[-1]
            return result
        self.log.ai("NO RESPONSE")
        return "NO RESPONSE"

    def close(self) -> None:
        # currently no explicit cleanup needed
        pass
