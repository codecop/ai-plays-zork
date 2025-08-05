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
        self.write_run_resource("system_prompt.md", system_prompt)

        self.agent = self.client.beta.agents.create(
            model=self.config()["model"],
            description=self.config()["description"],
            name=self.config()["name"],
            instructions=system_prompt,
            tools=self.config()["tools"],
        )

        self._log_agent_info()

    def _log_agent_info(self):
        self.log.ai(
            f"ai: {self.__class__}\n"
            + f"configuration: {self.configuration}\n"
            + f"model: {self.agent.model}\n"
            + f"agent id: {self.agent.id}\n"
            + f"name: {self.agent.name}\n"
            + f"description: {self.agent.description}"
        )

    def get_next_command(self, context: str) -> str:
        prompt = f"Game answers with {context}"
        response = self._send_initial_prompt_to_server(prompt)

        if not response.outputs or len(response.outputs) == 0:
            self.log.ai("NO RESPONSE")
            return "NO RESPONSE"

        if len(response.outputs) > 1:
            self.log.ai("WARN multiple responses " + str(response.outputs))

        output = response.outputs[0]
        if output.type == "message.output":
            self.calls += 1
            result = output.content
            return self._extract_command_from(result)
        else:
            self.log.ai("WARN not a message response " + str(output))
            return "NO RESPONSE"

    def _send_initial_prompt_to_server(self, prompt: str) -> str:
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
        return response

    def _extract_command_from(self, response: str) -> str:
        if "\n" in response:
            self.log.ai(response)
            response = response.splitlines()[-1]
        return response

    def close(self) -> None:
        # currently no explicit cleanup needed
        pass
